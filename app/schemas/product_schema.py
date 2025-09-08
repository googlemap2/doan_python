from typing import Optional

from pydantic import BaseModel


class CreateProduct(BaseModel):
    name: str
    description: str
    price: float
    brand_id: int
    color: str
    capacity: str
    image_url: Optional[str] = None
    compare_price: Optional[float] = None
    code: str
    is_active: Optional[bool] = False
