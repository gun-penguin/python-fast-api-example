from pydantic import BaseModel


class PageBaseSchema(BaseModel):
    page: int = 1
    size: int = 10

    def get_skip(self):
        return (self.page - 1) * self.size

    def get_limit(self):
        return self.size
