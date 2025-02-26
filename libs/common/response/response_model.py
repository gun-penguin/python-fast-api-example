from pydantic import BaseModel


class ResponseModel(BaseModel):
    code: int = 1
