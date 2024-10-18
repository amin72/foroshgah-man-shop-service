from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str | None
    price: int
    is_active: bool = True
    category_id: str
