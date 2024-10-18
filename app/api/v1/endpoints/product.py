from fastapi import APIRouter, HTTPException, Depends
from tortoise.exceptions import DoesNotExist
from tortoise.transactions import in_transaction

from app.models.category import ProductCategory
from app.models.product import Product
from app.models.shop import Shop
from app.schemas.product import ProductCreate
from app.schemas.token import TokenData
from app.utils import get_current_user

router = APIRouter()


@router.post("", response_model=ProductCreate)
async def add_product(
    product: ProductCreate,
    user: TokenData = Depends(get_current_user),  # noqa: ARG001
):
    shop = await Shop.get_or_none(owner_id=user.user_id)

    if shop is None:
        raise HTTPException(status_code=404, detail="Shop not found")

    # Validate the category if provided
    if product.category_id:
        category = await ProductCategory.get_or_none(id=product.category_id)

        if category is None:
            raise HTTPException(status_code=404, detail="Category not found")

    async with in_transaction():
        new_product = await Product.create(
            name=product.name,
            description=product.description,
            price=product.price,
            is_active=product.is_active,
            shop=shop,
            category=category,
        )

    return new_product
