from sqlalchemy import Column, DateTime, func

from libs.db.model.created_at_model import CreatedAtModel


class UpdatedAtModel(CreatedAtModel):
    __abstract__ = True  # 이 클래스 자체는 테이블로 생성되지 않음
    updated_at = Column(DateTime, default=func.now(), nullable=False)
