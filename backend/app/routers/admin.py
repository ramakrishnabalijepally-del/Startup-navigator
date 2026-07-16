from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.user import User
from app.models.article import Article
from app.models.resource import Resource
from app.models.search_history import SearchHistory
from app.dependencies import require_admin

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/analytics")
def analytics(db: Session = Depends(get_db), _admin=Depends(require_admin)):
    total_users = db.query(func.count(User.id)).scalar()
    total_articles = db.query(func.count(Article.id)).scalar()
    total_resources = db.query(func.count(Resource.id)).scalar()
    total_searches = db.query(func.count(SearchHistory.id)).scalar()

    popular_topics = (
        db.query(SearchHistory.category_hint, func.count(SearchHistory.id).label("cnt"))
        .filter(SearchHistory.category_hint.isnot(None))
        .group_by(SearchHistory.category_hint)
        .order_by(func.count(SearchHistory.id).desc())
        .limit(5)
        .all()
    )

    recent_searches = (
        db.query(SearchHistory)
        .order_by(SearchHistory.created_at.desc())
        .limit(10)
        .all()
    )

    return {
        "totals": {
            "users": total_users,
            "articles": total_articles,
            "resources": total_resources,
            "searches": total_searches,
        },
        "popular_topics": [{"category": r[0], "count": r[1]} for r in popular_topics],
        "recent_searches": [
            {"id": s.id, "query": s.query, "user_id": s.user_id, "created_at": s.created_at.isoformat()}
            for s in recent_searches
        ],
    }


@router.post("/reindex")
def reindex_all(background_tasks: BackgroundTasks, db: Session = Depends(get_db), _admin=Depends(require_admin)):
    """Re-embed all published articles into ChromaDB. Use after Render restarts wipe the disk."""
    articles = db.query(Article).filter(Article.is_published == 1).all()
    article_ids = [a.id for a in articles]
    background_tasks.add_task(_run_reindex, article_ids)
    return {"message": f"Reindexing {len(article_ids)} articles in background"}


def _run_reindex(article_ids: list[int]):
    try:
        from app.services.rag_service import get_rag_service
        from app.database import SessionLocal
        db = SessionLocal()
        from app.models.article import Article
        rag = get_rag_service()
        rag.reset_collection()
        for aid in article_ids:
            article = db.query(Article).filter(Article.id == aid).first()
            if article:
                rag.upsert_article(article)
        db.close()
        print(f"[RAG] Reindexed {len(article_ids)} articles successfully")
    except Exception as e:
        print(f"[RAG] Reindex failed: {e}")
