from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar('T')


class ResponseDataModel(BaseModel, Generic[T]):
    code: int = 1
    data: Optional[T] = None
