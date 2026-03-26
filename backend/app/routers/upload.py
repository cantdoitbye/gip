import os
import uuid
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.middleware.auth import CurrentUser
from app.schemas.upload import UploadResponse
from app.services.audit import log_action

router = APIRouter(prefix="/upload", tags=["upload"])

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".txt"}
MAX_FILE_SIZE = 10 * 1024 * 1024
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads")


def ensure_upload_dir():
    os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
    file: UploadFile = File(...),
) -> UploadResponse:
    ensure_upload_dir()
    
    filename = file.filename or "unknown"
    file_ext = os.path.splitext(filename)[1].lower()
    
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type .{file_ext} not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Maximum size: {MAX_FILE_SIZE / (1024 * 1024)}MB"
        )
    
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    with open(file_path, "wb") as f:
        f.write(content)
    
    file_url = f"/uploads/{unique_filename}"
    
    await log_action(
        db=db,
        user_id=current_user.id,
        action="file_uploaded",
        details={
            "filename": filename,
            "file_size": len(content),
            "file_type": file_ext,
        },
    )
    
    return UploadResponse(
        filename=filename,
        file_url=file_url,
        file_size=len(content),
        file_type=file_ext,
    )
