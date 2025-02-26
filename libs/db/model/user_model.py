from sqlalchemy import Column, Integer, String

from libs.db.model.updated_at_model import UpdatedAtModel


class UserModel(UpdatedAtModel):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
