from pydantic import BaseModel


class Brand(BaseModel):
    id: int
    name: str
