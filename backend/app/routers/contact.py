from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.contact import ContactSubmission
from app.schemas.contact import ContactCreate, ContactResponse
from app.dependencies import require_admin

router = APIRouter(prefix="/contact", tags=["contact"])


@router.post("", response_model=ContactResponse, status_code=201)
def submit_contact(body: ContactCreate, db: Session = Depends(get_db)):
    submission = ContactSubmission(**body.model_dump())
    db.add(submission)
    db.commit()
    db.refresh(submission)
    return submission


@router.get("", response_model=List[ContactResponse])
def list_submissions(
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    return db.query(ContactSubmission).order_by(ContactSubmission.created_at.desc()).offset(offset).limit(limit).all()
