from sqlalchemy import Column, Integer, String

from libs.db.model.updated_at_model import UpdatedAtModel


class ItemModel(UpdatedAtModel):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
