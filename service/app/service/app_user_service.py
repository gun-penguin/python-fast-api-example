from sqlalchemy.ext.asyncio import AsyncSession

from libs.common.schema.page_base_schema import PageBaseSchema
from libs.db.config.db_config import transactional
from service.app.repository.app_user_repository import AppUserRepository
from service.app.schema.app_user_schema import AppUserSchema


class AppUserService:
    @staticmethod
    @transactional(readonly=True)
    async def get_user(user_id: int, db: AsyncSession):
        user = await AppUserRepository.get_user(db, user_id)
        return AppUserSchema.model_validate(user)

    @staticmethod
    @transactional(readonly=True)
    async def get_user_count(db: AsyncSession):
        return await AppUserRepository.get_user_count(db)

    @staticmethod
    @transactional(readonly=True)
    async def get_user_list(page_info:PageBaseSchema, db: AsyncSession):
        user_list = await AppUserRepository.get_user_list(db, page_info.get_skip(), page_info.get_limit())
        return [AppUserSchema.model_validate(user) for user in user_list]

    @staticmethod
    @transactional(readonly=False)
    async def create_user(user: AppUserSchema, db: AsyncSession):
        user = await AppUserRepository.create_user(db, user)
        if user.id > 0:
            return True
        return False
