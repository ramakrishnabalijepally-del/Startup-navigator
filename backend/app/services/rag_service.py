"""
RAG service: LangChain + ChromaDB + Google Gemini.

Embedding: gemini-embedding-004 (via langchain-google-genai)
Generation: gemini-2.0-flash

ChromaDB is file-persisted at settings.chroma_persist_dir.
NOTE for Render free tier: the disk resets on every restart. Call POST /admin/reindex
after each deploy to rebuild the vector store from the PostgreSQL articles table.
"""
from __future__ import annotations

import functools
import json
from typing import TYPE_CHECKING

from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.prompts import ChatPromptTemplate

from app.config import get_settings

if TYPE_CHECKING:
    from app.models.article import Article

settings = get_settings()

print("========== STARTUP CONFIG ==========")
print("Embedding model:", settings.gemini_embedding_model)
print("Generation model:", settings.gemini_generation_model)
print("====================================")

SYSTEM_PROMPT = """You are Startup Navigator's AI assistant. Your job is to help entrepreneurs
with questions about starting, funding, and growing their businesses.

Answer the question using ONLY the context provided below. Be specific, practical, and cite
relevant details from the context. If the answer is not found in the context, say:
"I don't have enough information in my knowledge base to answer that. Try rephrasing your
question or browse the Explore Topics section."

Do not make up information. Do not use prior training knowledge about specific laws or
regulations without grounding it in the provided context.

Context:
{context}
"""

HUMAN_PROMPT = "Question: {question}"


class RAGService:
    def __init__(self):
        self._embeddings = GoogleGenerativeAIEmbeddings(
            model=settings.gemini_embedding_model,
            google_api_key=settings.google_api_key,
        )
        self._llm = ChatGoogleGenerativeAI(
            model=settings.gemini_generation_model,
            google_api_key=settings.google_api_key,
            temperature=0.2,
        )
        self._vectorstore = Chroma(
            collection_name=settings.chroma_collection_name,
            embedding_function=self._embeddings,
            persist_directory=settings.chroma_persist_dir,
        )
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150,
            separators=["\n\n", "\n", ". ", " ", ""],
        )
        self._prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("human", HUMAN_PROMPT),
        ])

    # ------------------------------------------------------------------ #
    # Indexing                                                             #
    # ------------------------------------------------------------------ #

    def upsert_article(self, article: "Article") -> None:
        """Chunk and embed a single article, replacing any existing chunks."""
        self.delete_article(article.id)
        chunks = self._splitter.split_text(article.content)
        docs = [
            Document(
                page_content=chunk,
                metadata={
                    "article_id": str(article.id),
                    "title": article.title,
                    "category": article.category,
                    "tags": json.dumps(article.tags or []),
                },
            )
            for chunk in chunks
        ]
        if docs:
            ids = [f"art{article.id}_chunk{i}" for i in range(len(docs))]
            self._vectorstore.add_documents(docs, ids=ids)

    def delete_article(self, article_id: int) -> None:
        """Remove all chunks for an article from ChromaDB."""
        try:
            collection = self._vectorstore._collection
            existing = collection.get(where={"article_id": str(article_id)})
            if existing and existing["ids"]:
                collection.delete(ids=existing["ids"])
        except Exception:
            pass  # Collection may be empty on first run

    def reset_collection(self) -> None:
        """Delete all documents — used before a full reindex."""
        try:
            self._vectorstore._collection.delete(where={})
        except Exception:
            pass

    # ------------------------------------------------------------------ #
    # Retrieval + Generation                                               #
    # ------------------------------------------------------------------ #

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True,
    )
    def search(self, query: str) -> dict:
        """
        Embed query → retrieve top-k chunks → generate answer.
        Returns: {answer, sources: [{article_id, title, category, excerpt}]}
        """
        import traceback as _tb

        docs_with_scores = self._vectorstore.similarity_search_with_relevance_scores(
            query, k=settings.rag_top_k
        )

        if not docs_with_scores:
            return {
                "answer": "I don't have enough information in my knowledge base to answer that. "
                          "Try browsing the Explore Topics section for relevant articles.",
                "sources": [],
                "category_hint": None,
            }

        # De-duplicate by article_id, keep highest-score chunk per article
        seen: dict[str, dict] = {}
        for doc, score in docs_with_scores:
            aid = doc.metadata.get("article_id", "unknown")
            if aid not in seen or score > seen[aid]["score"]:
                seen[aid] = {"doc": doc, "score": score}

        top_docs = [v["doc"] for v in seen.values()]
        context = "\n\n---\n\n".join(
            f"[{d.metadata.get('title', 'Article')} | {d.metadata.get('category', '')}]\n{d.page_content}"
            for d in top_docs
        )

        # ── DEBUG: log model identity before calling Gemini ──────────────
        api_key_prefix = (settings.google_api_key or "")[:8]
        llm_model_attr = getattr(self._llm, "model", None) or getattr(self._llm, "model_name", None)
        print("===== RAG DEBUG: PRE-INVOKE =====")
        print(f"  settings.gemini_generation_model : {settings.gemini_generation_model}")
        print(f"  settings.gemini_embedding_model  : {settings.gemini_embedding_model}")
        print(f"  self._llm                        : {self._llm!r}")
        print(f"  self._llm model attr             : {llm_model_attr}")
        print(f"  google_api_key prefix (8 chars)  : {api_key_prefix}...")
        print("=================================")
        # ─────────────────────────────────────────────────────────────────

        chain = self._prompt | self._llm
        try:
            result = chain.invoke({"context": context, "question": query})
        except Exception as exc:
            print("===== RAG DEBUG: INVOKE FAILED =====")
            print(f"  generation model : {settings.gemini_generation_model}")
            print(f"  embedding model  : {settings.gemini_embedding_model}")
            print(f"  exception repr   : {exc!r}")
            print(f"  traceback:\n{_tb.format_exc()}")
            print("====================================")
            raise

        answer = result.content if hasattr(result, "content") else str(result)

        sources = [
            {
                "article_id": int(d.metadata["article_id"]) if d.metadata.get("article_id", "").isdigit() else None,
                "title": d.metadata.get("title", ""),
                "category": d.metadata.get("category", ""),
                "excerpt": d.page_content[:200] + "…" if len(d.page_content) > 200 else d.page_content,
            }
            for d in top_docs
        ]

        # Best-guess category from top result
        category_hint = top_docs[0].metadata.get("category") if top_docs else None

        return {"answer": answer, "sources": sources, "category_hint": category_hint}


@functools.lru_cache(maxsize=1)
def get_rag_service() -> RAGService:
    """Singleton — instantiated once per process."""
    return RAGService()
