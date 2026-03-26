from typing import Any
import uuid
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit import AuditLog


async def log_action(
    db: AsyncSession,
    user_id: uuid.UUID | None,
    action: str,
    details: dict[str, Any] | None = None,
    ip_address: str | None = None,
) -> AuditLog:
    audit_log = AuditLog(
        user_id=user_id,
        action=action,
        details=details,
        ip_address=ip_address,
        timestamp=datetime.utcnow(),
    )
    db.add(audit_log)
    return audit_log
