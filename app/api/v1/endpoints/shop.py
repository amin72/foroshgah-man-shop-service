from fastapi import APIRouter, Depends, HTTPException, Request
from tortoise.expressions import Q

from app.models.category import Category
from app.models.shop import Shop
from app.schemas.shop import ShopList, ShopUpdate, ShopReadPrivate
from app.schemas.token import TokenData
from app.utils import get_current_user

router = APIRouter()


@router.get("")
async def get_my_shop_api(
    user: TokenData = Depends(get_current_user),  # noqa: ARG001
) -> ShopReadPrivate:
    """Get shop info"""

    shop = await Shop.get_or_none(owner_id=user.user_id)
    if shop is None:
        raise HTTPException(status_code=404, detail="Shop not found")

    return shop


@router.patch("")
async def update_shop_api(
    request: Request,  # noqa: ARG001
    data: ShopUpdate,
    user: TokenData = Depends(get_current_user),  # noqa: ARG001
) -> ShopUpdate:
    """Update shop info"""

    shop = await Shop.get_or_none(owner_id=user.user_id)

    if shop is None:
        raise HTTPException(status_code=404, detail="Shop not found")

    shop_data = data.model_dump()
    category_id = shop_data.get("category_id")

    if category_id:
        category = await Category.get_or_none(id=category_id)
        if category is not None:
            shop_data["category"] = category

    await shop.update_from_dict(shop_data).save()

    return shop_data


@router.get("/home")
async def home_api(
    user: TokenData = Depends(get_current_user),  # noqa: ARG001
) -> dict[str, list[ShopList]]:
    """Get shops for home API"""

    newest_shops = await Shop.all().order_by("-id").limit(8)
    newest_shops = list(newest_shops)
    result = {
        "newest": newest_shops,
        "paid": [],
        "starred": [],
        "active": [],
    }

    return result


# TODO: Pagination


@router.get("/{category_id}")
async def list_shops_api(
    category_id: str,
    is_physical: bool | None = None,
    user: TokenData = Depends(get_current_user),  # noqa: ARG001
) -> list[ShopList]:
    """List shops in category API"""

    filters = Q(category_id=category_id)

    if is_physical is not None:
        filters &= Q(is_physical=is_physical)

    shops = await Shop.filter(filters)
    return shops
