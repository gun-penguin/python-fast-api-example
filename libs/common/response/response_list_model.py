from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel

T = TypeVar('T')


class ResponseListModel(BaseModel, Generic[T]):
    code: int = 1
    list: Optional[List[T]] = None
    count: int = 0
