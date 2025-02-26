from sqlalchemy import select, func, insert
from sqlalchemy.ext.asyncio import AsyncSession

from libs.db.model.user_model import UserModel
from sqlalchemy.sql.base import Executable

from service.app.schema.app_user_schema import AppUserSchema


class AppUserRepository:
    @staticmethod
    async def get_user(db: AsyncSession, user_id: int):
        query: Executable = select(UserModel.__table__).where(UserModel.id == user_id).limit(1)
        result = await db.execute(query)
        return result.fetchone()

    @staticmethod
    async def get_user_list(db: AsyncSession, skip: int = 0, size: int = 10):
        query: Executable = select(UserModel.__table__).limit(size).offset(skip)
        result = await db.execute(query)
        return result.fetchall()

    @staticmethod
    async def get_user_count(db: AsyncSession):
        query: Executable = select(func.count()).select_from(UserModel.__table__)
        result = await db.execute(query)
        return result.scalar()

    @staticmethod
    async def create_user(db: AsyncSession, user: AppUserSchema):
        query: Executable = insert(UserModel).values(name=user.name).returning(UserModel.id)
        result = await db.execute(query)
        return result.fetchone()
