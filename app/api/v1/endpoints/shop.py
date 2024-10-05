from fastapi import APIRouter

router = APIRouter()


@router.get("")
async def get_api():
    """API to get info."""
    return "Shop APIs"
