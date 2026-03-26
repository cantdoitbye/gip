import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import select, update
from app.database import async_session_maker
from app.models.user import User

async def update_emails():
    email_mapping = {
        "admin@infrastructure.ap.gov.in": "admin@ooumph.com",
        "planner@infrastructure.ap.gov.in": "planner@ooumph.com",
        "viewer@infrastructure.ap.gov.in": "viewer@ooumph.com",
    }

    async with async_session_maker() as db:
        print("Updating user emails...")
        print("-" * 40)

        for old_email, new_email in email_mapping.items():
            result = await db.execute(select(User).where(User.email == old_email))
            user = result.scalar_one_or_none()

            if user:
                user.email = new_email
                print(f"Updated: {old_email} -> {new_email}")
            else:
                print(f"Not found: {old_email}")

        await db.commit()
        print("-" * 40)
        print("Email update completed!")

if __name__ == "__main__":
    asyncio.run(update_emails())
