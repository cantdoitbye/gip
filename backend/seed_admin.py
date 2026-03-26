import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import select
from app.database import engine, async_session_maker, Base
from app.models.user import User, UserRole
from app.utils.security import hash_password

async def seed_users():
    print("Creating all database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_maker() as db:
        demo_users = [
        {
            "email": "admin@ooumph.com",
            "password": "admin123",
            "full_name": "System Administrator",
            "role": UserRole.admin,
        },
        {
            "email": "planner@ooumph.com",
            "password": "planner123",
            "full_name": "Infrastructure Planner",
            "role": UserRole.planner,
        },
        {
            "email": "viewer@ooumph.com",
            "password": "viewer123",
            "full_name": "Demo Viewer",
            "role": UserRole.viewer,
        },
    ]

        print("\n------------------------------")
        print("Demo Users Setup")
        print("------------------------------")

        for user_data in demo_users:
            result = await db.execute(select(User).where(User.email == user_data["email"]))
            existing_user = result.scalar_one_or_none()

            if existing_user:
                print(f"User {user_data['email']} already exists (Role: {user_data['role'].value})")
            else:
                new_user = User(
                    email=user_data["email"],
                    hashed_password=hash_password(user_data["password"]),
                    full_name=user_data["full_name"],
                    role=user_data["role"],
                    is_active=True,
                )
                db.add(new_user)
                print(f"Created user: {user_data['email']} (Role: {user_data['role'].value})")

        await db.commit()

        print("\n------------------------------")
        print("Demo Credentials for Login:")
        print("------------------------------")
        print("\nAdministrator:")
        print("  Email: admin@ooumph.com")
        print("  Password: admin123")
        print("\nInfrastructure Planner:")
        print("  Email: planner@ooumph.com")
        print("  Password: planner123")
        print("\nViewer:")
        print("  Email: viewer@ooumph.com")
        print("  Password: viewer123")
        print("\n------------------------------")

if __name__ == "__main__":
    asyncio.run(seed_users())
