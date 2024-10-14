from fastapi import APIRouter, Depends, Request

from app.models.category import Category
from app.schemas.category import CategoryRead
from app.schemas.token import TokenData
from app.utils import get_current_user

router = APIRouter()


@router.get("")
async def list_category_api(
    request: Request,  # noqa: ARG001
    user: TokenData = Depends(get_current_user),  # noqa: ARG001
) -> list[CategoryRead]:
    """List of categories"""

    categories = await Category.all()
    return categories
