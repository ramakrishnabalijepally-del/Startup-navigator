from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.resource import Resource
from app.schemas.resource import ResourceCreate, ResourceUpdate, ResourceResponse
from app.dependencies import require_admin

router = APIRouter(prefix="/resources", tags=["resources"])


@router.get("", response_model=List[ResourceResponse])
def list_resources(
    category: Optional[str] = Query(None),
    resource_type: Optional[str] = Query(None),
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    q = db.query(Resource).filter(Resource.is_active == 1)
    if category:
        q = q.filter(Resource.category == category)
    if resource_type:
        q = q.filter(Resource.resource_type == resource_type)
    return q.order_by(Resource.created_at.desc()).offset(offset).limit(limit).all()


@router.get("/{resource_id}", response_model=ResourceResponse)
def get_resource(resource_id: int, db: Session = Depends(get_db)):
    r = db.query(Resource).filter(Resource.id == resource_id, Resource.is_active == 1).first()
    if not r:
        raise HTTPException(status_code=404, detail="Resource not found")
    return r


@router.post("", response_model=ResourceResponse, status_code=201)
def create_resource(body: ResourceCreate, db: Session = Depends(get_db), _admin=Depends(require_admin)):
    r = Resource(**body.model_dump())
    db.add(r)
    db.commit()
    db.refresh(r)
    return r


@router.put("/{resource_id}", response_model=ResourceResponse)
def update_resource(
    resource_id: int, body: ResourceUpdate,
    db: Session = Depends(get_db), _admin=Depends(require_admin),
):
    r = db.query(Resource).filter(Resource.id == resource_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Resource not found")
    for field, val in body.model_dump(exclude_none=True).items():
        setattr(r, field, val)
    db.commit()
    db.refresh(r)
    return r


@router.delete("/{resource_id}", status_code=204)
def delete_resource(resource_id: int, db: Session = Depends(get_db), _admin=Depends(require_admin)):
    r = db.query(Resource).filter(Resource.id == resource_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Resource not found")
    db.delete(r)
    db.commit()
