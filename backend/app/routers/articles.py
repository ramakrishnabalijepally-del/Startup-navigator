from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.article import Article
from app.schemas.article import ArticleCreate, ArticleUpdate, ArticleResponse, ArticleListResponse
from app.dependencies import get_current_user, require_admin

router = APIRouter(prefix="/articles", tags=["articles"])

VALID_CATEGORIES = [
    "Registration", "Funding", "Legal", "Hiring", "Branding",
    "Marketing", "Taxation", "Fundraising", "AI Tools", "Growth",
]


@router.get("", response_model=List[ArticleListResponse])
def list_articles(
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    q = db.query(Article).filter(Article.is_published == 1)
    if category:
        q = q.filter(Article.category == category)
    if search:
        q = q.filter(Article.title.ilike(f"%{search}%"))
    return q.order_by(Article.created_at.desc()).offset(offset).limit(limit).all()


@router.get("/{article_id}", response_model=ArticleResponse)
def get_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id, Article.is_published == 1).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@router.post("", response_model=ArticleResponse, status_code=201)
def create_article(
    body: ArticleCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    article = Article(**body.model_dump())
    db.add(article)
    db.commit()
    db.refresh(article)
    # Re-index in background so response is instant
    background_tasks.add_task(_reindex_article, article.id)
    return article


@router.put("/{article_id}", response_model=ArticleResponse)
def update_article(
    article_id: int,
    body: ArticleUpdate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    for field, val in body.model_dump(exclude_none=True).items():
        setattr(article, field, val)
    db.commit()
    db.refresh(article)
    background_tasks.add_task(_reindex_article, article.id)
    return article


@router.delete("/{article_id}", status_code=204)
def delete_article(
    article_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    db.delete(article)
    db.commit()
    background_tasks.add_task(_remove_from_index, article_id)


def _reindex_article(article_id: int):
    """Background task: re-embed a single article into ChromaDB."""
    try:
        from app.services.rag_service import get_rag_service
        from app.database import SessionLocal
        db = SessionLocal()
        article = db.query(Article).filter(Article.id == article_id).first()
        if article:
            rag = get_rag_service()
            rag.upsert_article(article)
        db.close()
    except Exception as e:
        print(f"[RAG] reindex error for article {article_id}: {e}")


def _remove_from_index(article_id: int):
    try:
        from app.services.rag_service import get_rag_service
        rag = get_rag_service()
        rag.delete_article(article_id)
    except Exception as e:
        print(f"[RAG] delete index error for article {article_id}: {e}")
