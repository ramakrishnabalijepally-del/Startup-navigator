from fastapi import APIRouter, Depends, HTTPException, Response, Cookie, status
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, TokenResponse
from app.services.auth_service import (
    hash_password, verify_password,
    create_access_token, create_refresh_token, decode_token,
)
from app.dependencies import get_current_user
from app.config import get_settings

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()

_prod = settings.environment == "production"
COOKIE_OPTS = dict(
    httponly=True,
    samesite="none" if _prod else "lax",
    secure=_prod,
    path="/",
)


@router.post("/register", response_model=TokenResponse, status_code=201)
def register(body: UserCreate, response: Response, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == body.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=body.email,
        hashed_password=hash_password(body.password),
        full_name=body.full_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    _set_auth_cookies(response, user)
    return TokenResponse(
        access_token=create_access_token(user.id, user.role.value),
        user=UserResponse.model_validate(user),
    )


@router.post("/login", response_model=TokenResponse)
def login(body: UserLogin, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == body.email).first()
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account deactivated")

    _set_auth_cookies(response, user)
    return TokenResponse(
        access_token=create_access_token(user.id, user.role.value),
        user=UserResponse.model_validate(user),
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh(
    response: Response,
    refresh_token: Optional[str] = Cookie(default=None),
    db: Session = Depends(get_db),
):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token")

    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user = db.query(User).filter(User.id == int(payload["sub"]), User.is_active == True).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    _set_auth_cookies(response, user)
    return TokenResponse(
        access_token=create_access_token(user.id, user.role.value),
        user=UserResponse.model_validate(user),
    )


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token", **COOKIE_OPTS)
    response.delete_cookie("refresh_token", **COOKIE_OPTS)
    return {"message": "Logged out"}


@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)


def _set_auth_cookies(response: Response, user: User):
    access = create_access_token(user.id, user.role.value)
    refresh = create_refresh_token(user.id)
    response.set_cookie("access_token", access, max_age=60 * settings.access_token_expire_minutes, **COOKIE_OPTS)
    response.set_cookie("refresh_token", refresh, max_age=60 * 60 * 24 * settings.refresh_token_expire_days, **COOKIE_OPTS)
