from pydantic import BaseModel


class CategoryRead(BaseModel):
    id: str
    title: str
    image: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "01F8MECHZX3TBDSZ7XRADM79XV",
                    "name": "Category name",
                    "image": "URL",
                }
            ]
        }
    }
