from typing import Any
import uuid

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, UserRole
from app.schemas.auth import Token
from app.schemas.user import UserCreate
from app.utils.security import hash_password, verify_password
from app.utils.jwt import (
    create_access_token,
    create_refresh_token,
    decode_token,
    is_token_blacklisted,
    blacklist_token,
)


async def register_user(db: AsyncSession, user_data: UserCreate) -> User:
    result = await db.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Email already registered",
        )

    hashed_password = hash_password(user_data.password)
    user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        role=UserRole.viewer,
        is_active=True,
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user


async def authenticate_user(db: AsyncSession, email: str, password: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    if not user.is_active:
        return None
    return user


def create_tokens(user: User) -> Token:
    token_data: dict[str, Any] = {
        "sub": str(user.id),
        "email": user.email,
        "role": user.role.value,
    }
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


async def refresh_tokens(refresh_token: str) -> Token:
    if await is_token_blacklisted(refresh_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = decode_token(refresh_token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )

    await blacklist_token(refresh_token)

    token_data: dict[str, Any] = {
        "sub": payload["sub"],
        "email": payload["email"],
        "role": payload["role"],
    }
    new_access_token = create_access_token(token_data)
    new_refresh_token = create_refresh_token(token_data)
    return Token(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
    )


async def logout_user(refresh_token: str) -> None:
    try:
        payload = decode_token(refresh_token)
        if payload.get("type") == "refresh":
            await blacklist_token(refresh_token)
    except Exception:
        pass
