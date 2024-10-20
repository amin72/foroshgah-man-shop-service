from fastapi import APIRouter, HTTPException, Depends, Request

from app.models.category import ProductCategory, ShopCategory
from app.schemas.category import ProductCategoryRead, ShopCategoryRead
from app.schemas.token import TokenData
from app.utils import get_current_user

router = APIRouter()


@router.get("")
async def list_shop_category_api(
    request: Request,  # noqa: ARG001
    user: TokenData = Depends(get_current_user),  # noqa: ARG001
) -> list[ShopCategoryRead]:
    """List of shop categories"""

    categories = await ShopCategory.filter(is_active=True)
    return categories


@router.get("/{id}")
async def list_product_category_api(
    id: str,
    request: Request,  # noqa: ARG001
    user: TokenData = Depends(get_current_user),  # noqa: ARG001
) -> list[ProductCategoryRead]:
    """List of product categories"""

    shop_category = await ShopCategory.get_or_none(id=id)

    if shop_category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    categories = await ProductCategory.filter(
        shop_category=shop_category, is_active=True
    )
    return categories
