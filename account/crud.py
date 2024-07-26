from sqlalchemy.ext.asyncio import AsyncEngine

from sqlalchemy import select, text
from sqlalchemy.orm import load_only
from account.models import User
from account.schemas import User as user_schema


async def get_user_with_password(db: AsyncEngine, username: str):
    async with db.connect() as db:
        query = select(User).where(User.username == username)
        user = await db.execute(query)
    return user.first()


async def get_user(db: AsyncEngine, user_id: int):
    async with db.connect() as db:
        query = select(User).options(
            load_only(User.id, User.username, User.full_name, User.email, User.is_active, User.user_type)
        ).where(User.id == user_id)
        user = await db.execute(query)
        user = user.first()
    return user


