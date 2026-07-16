from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.database import get_db
from app.models.search_history import SearchHistory
from app.models.user import User
from app.schemas.search import SearchHistoryResponse
from app.dependencies import get_current_user

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/me")
def my_dashboard(
    limit: int = Query(20, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    history = (
        db.query(SearchHistory)
        .filter(SearchHistory.user_id == current_user.id)
        .order_by(SearchHistory.created_at.desc())
        .limit(limit)
        .all()
    )
    total_searches = db.query(func.count(SearchHistory.id)).filter(SearchHistory.user_id == current_user.id).scalar()

    # Most searched category
    top_category = (
        db.query(SearchHistory.category_hint, func.count(SearchHistory.id).label("cnt"))
        .filter(SearchHistory.user_id == current_user.id, SearchHistory.category_hint.isnot(None))
        .group_by(SearchHistory.category_hint)
        .order_by(func.count(SearchHistory.id).desc())
        .first()
    )

    return {
        "user": {"id": current_user.id, "email": current_user.email, "full_name": current_user.full_name},
        "stats": {
            "total_searches": total_searches,
            "most_searched_category": top_category[0] if top_category else None,
            "last_active": history[0].created_at.isoformat() if history else None,
        },
        "search_history": [SearchHistoryResponse.model_validate(h) for h in history],
    }
