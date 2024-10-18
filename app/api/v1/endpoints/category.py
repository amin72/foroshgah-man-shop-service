from fastapi import APIRouter, Depends, Request

from app.models.category import ProductCategory, ShopCategory
from app.schemas.category import ProductCategoryRead, ShopCategoryRead
from app.schemas.token import TokenData
from app.utils import get_current_user

router = APIRouter()


@router.get("/shop")
async def list_shop_category_api(
    request: Request,  # noqa: ARG001
    user: TokenData = Depends(get_current_user),  # noqa: ARG001
) -> list[ShopCategoryRead]:
    """List of shop categories"""

    categories = await ShopCategory.filter(is_active=True)
    return categories


@router.get("/product")
async def list_product_category_api(
    request: Request,  # noqa: ARG001
    user: TokenData = Depends(get_current_user),  # noqa: ARG001
) -> list[ProductCategoryRead]:
    """List of product categories"""

    categories = await ProductCategory.filter(is_active=True)
    return categories
