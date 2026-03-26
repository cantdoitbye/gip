from typing import Annotated
import uuid

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.auth import Token, LoginRequest, RegisterRequest
from app.schemas.user import UserResponse
from app.services.auth import (
    register_user,
    authenticate_user,
    create_tokens,
    refresh_tokens,
    logout_user,
)
from app.services.audit import log_action

router = APIRouter(prefix="/auth", tags=["authentication"])


def get_client_ip(request: Request) -> str | None:
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else None


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(
    request: Request,
    user_data: RegisterRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Token:
    user = await register_user(db, user_data)
    tokens = create_tokens(user)
    ip_address = get_client_ip(request)
    await log_action(
        db=db,
        user_id=user.id,
        action="user_registered",
        details={"email": user.email, "full_name": user.full_name},
        ip_address=ip_address,
    )
    return tokens


@router.post("/login", response_model=Token)
async def login(
    request: Request,
    credentials: LoginRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Token:
    user = await authenticate_user(db, credentials.email, credentials.password)
    ip_address = get_client_ip(request)
    
    if not user:
        await log_action(
            db=db,
            user_id=None,
            action="login_failed",
            details={"email": credentials.email, "reason": "invalid_credentials"},
            ip_address=ip_address,
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    tokens = create_tokens(user)
    await log_action(
        db=db,
        user_id=user.id,
        action="login_success",
        details={"email": user.email},
        ip_address=ip_address,
    )
    return tokens


@router.post("/refresh", response_model=Token)
async def refresh(
    request: Request,
    refresh_token_data: dict,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Token:
    refresh_token = refresh_token_data.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="refresh_token is required",
        )
    
    tokens = await refresh_tokens(refresh_token)
    ip_address = get_client_ip(request)
    await log_action(
        db=db,
        user_id=uuid.UUID(decode_token_safe(refresh_token).get("sub", "")) if refresh_token else None,
        action="token_refreshed",
        details={},
        ip_address=ip_address,
    )
    return tokens


def decode_token_safe(token: str) -> dict:
    from app.utils.jwt import decode_token
    try:
        return decode_token(token)
    except Exception:
        return {}


@router.post("/logout")
async def logout(
    request: Request,
    logout_data: dict,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict:
    refresh_token = logout_data.get("refresh_token")
    if refresh_token:
        await logout_user(refresh_token)
    
    ip_address = get_client_ip(request)
    await log_action(
        db=db,
        user_id=None,
        action="logout",
        details={},
        ip_address=ip_address,
    )
    
    return {"message": "Successfully logged out"}
