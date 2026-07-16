import traceback
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.search_history import SearchHistory
from app.models.user import User
from app.schemas.search import SearchRequest, SearchResponse, SourceDoc
from app.dependencies import get_current_user
from app.services.rag_service import get_rag_service

router = APIRouter(prefix="/search", tags=["search"])


def _classify_error(e: Exception) -> str:
    msg = str(e).lower()
    name = type(e).__name__
    if "resourceexhausted" in name.lower() or "429" in msg or "quota" in msg:
        return "Gemini quota exhausted (rate limit or daily limit). Wait and retry."
    if "notfound" in name.lower() or "404" in msg or "is not found" in msg:
        return f"Gemini model not found — check GEMINI_EMBEDDING_MODEL / GEMINI_GENERATION_MODEL in .env. Detail: {e}"
    if "unauthenticated" in name.lower() or "401" in msg or "api key" in msg.lower():
        return "Invalid GOOGLE_API_KEY — check your .env file."
    if "permissiondenied" in name.lower() or "403" in msg:
        return "Gemini API key does not have permission for this model."
    return f"{name}: {e}"


@router.post("", response_model=SearchResponse)
def rag_search(
    body: SearchRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not body.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    try:
        rag = get_rag_service()
        result = rag.search(body.query)
    except Exception as e:
        classified = _classify_error(e)
        print(f"\n[SEARCH ERROR] {classified}")
        print(f"[SEARCH ERROR] repr: {repr(e)}")
        traceback.print_exc()
        raise HTTPException(
            status_code=503,
            detail=f"AI search is temporarily unavailable: {classified}",
        )

    history = SearchHistory(
        user_id=current_user.id,
        query=body.query,
        answer=result["answer"],
        sources=result["sources"],
        category_hint=result.get("category_hint"),
    )
    db.add(history)
    db.commit()
    db.refresh(history)

    return SearchResponse(
        query=body.query,
        answer=result["answer"],
        sources=[SourceDoc(**s) for s in result["sources"]],
        history_id=history.id,
    )
