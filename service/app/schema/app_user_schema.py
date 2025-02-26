from pydantic import BaseModel, ConfigDict


class AppUserSchema(BaseModel):
    id: int = 0
    name: str = None

    model_config = ConfigDict(from_attributes=True)
