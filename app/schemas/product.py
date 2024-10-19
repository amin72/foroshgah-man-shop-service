from pydantic import BaseModel


product_model_config = {
    "json_schema_extra": {
        "examples": [
            {
                "name": "Shop name",
                "description": "Shop description",
                "price": 100000,
                "is_active": True,
                "category_id": "01F8MECHZX3TBDSZ7XRADM79XV",
            }
        ]
    }
}


class ProductCreate(BaseModel):
    name: str
    description: str | None
    price: int
    is_active: bool = True
    category_id: str

    model_config = product_model_config


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: int | None = None
    is_active: bool | None = None
    category_id: str | None = None

    model_config = product_model_config
