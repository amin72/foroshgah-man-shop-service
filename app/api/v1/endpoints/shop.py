from fastapi import APIRouter, Depends, Request

from app.models.shop import Shop
from app.schemas.shop import ShopUpdate
from app.schemas.token import TokenData
from app.utils import get_current_user

router = APIRouter()


@router.patch("")
async def update_shop_api(
    request: Request,  # noqa: ARG001
    data: ShopUpdate,
    user: TokenData = Depends(get_current_user),  # noqa: ARG001
) -> ShopUpdate:
    """Update shop info"""

    shop = await Shop.get_or_none(owner_id=user.user_id)
    await shop.update_from_dict(data.model_dump()).save()

    return data
