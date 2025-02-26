from sqlalchemy import Column, DateTime, func

from libs.db.config.db_config import DbConfig


class CreatedAtModel(DbConfig.db_model_base):
    __abstract__ = True  # 이 클래스 자체는 테이블로 생성되지 않음
    created_at = Column(DateTime, default=func.now(), nullable=False)
