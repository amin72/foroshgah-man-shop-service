from pydantic import BaseModel


def category_example(title: str = "Category name", include_shop_category: bool = False):
    """Utility function to generate example configurations"""

    example = {
        "id": "01F8MECHZX3TBDSZ7XRADM79XV",
        "title": title,
        "image": "URL",
    }

    if include_shop_category:
        example["shop_category_id"] = "02F8MECHZX3TBDSZ7XRADM70XV"

    return {"json_schema_extra": {"examples": [example]}}


class CategoryRead(BaseModel):
    id: str
    title: str
    image: str

    model_config = category_example()


class ShopCategoryRead(CategoryRead):
    pass


class ProductCategoryRead(CategoryRead):
    shop_category_id: str

    model_config = category_example(include_shop_category=True)
