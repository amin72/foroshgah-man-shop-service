from fastapi import APIRouter, HTTPException, Depends, status
from tortoise.exceptions import DoesNotExist
from tortoise.transactions import in_transaction

from app.models.category import ProductCategory
from app.models.product import Product
from app.models.shop import Shop
from app.schemas.product import ProductCreate, ProductUpdate
from app.schemas.token import TokenData
from app.utils import get_current_user

router = APIRouter()


@router.post("", response_model=ProductCreate)
async def add_product_api(
    product: ProductCreate,
    user: TokenData = Depends(get_current_user),
):
    """
    Create product API
    """

    shop = await Shop.get_or_none(owner_id=user.user_id)

    if shop is None:
        raise HTTPException(status_code=404, detail="Shop not found")

    # Check category
    product_category = await ProductCategory.get_or_none(id=product.category_id)

    if product_category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    product_shop_category_id = (await product_category.shop_category).id
    shop_category_id = (await shop.category).id

    if product_shop_category_id != shop_category_id:
        raise HTTPException(status_code=400, detail="Wrong category")

    async with in_transaction():
        new_product = await Product.create(
            name=product.name,
            description=product.description,
            price=product.price,
            is_active=product.is_active,
            shop=shop,
            category=product_category,
        )

    return new_product


@router.patch("/{id}", response_model=ProductUpdate)
async def update_product_api(
    id: str,
    product: ProductUpdate,
    user: TokenData = Depends(get_current_user),
):
    """
    Update product API
    """

    shop = await Shop.get_or_none(owner_id=user.user_id)

    if shop is None:
        raise HTTPException(status_code=404, detail="Shop not found")

    product_obj = await Product.get_or_none(id=id)

    if product_obj is None:
        raise HTTPException(status_code=404, detail="Product not found")

    if product_obj.shop_id != shop.id:
        raise HTTPException(status_code=404, detail="Product not found")

    product_data: dict = product.model_dump()

    if product.is_active is None:
        del product_data["is_active"]

    # Check category
    product_category = await ProductCategory.get(id=product.category_id)

    product_shop_category_id = (await product_category.shop_category).id
    shop_category_id = (await shop.category).id

    if product_shop_category_id != shop_category_id:
        raise HTTPException(status_code=400, detail="Wrong category")

    # Validate the category if provided
    if product.category_id:
        category = await ProductCategory.get_or_none(id=product.category_id)

        if category is None:
            raise HTTPException(status_code=404, detail="Category not found")

        product_data["category"] = category

    await product_obj.update_from_dict(product_data).save()

    return product_obj


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_api(
    id: str,
    user: TokenData = Depends(get_current_user),
):
    """
    Delete product API
    """

    shop = await Shop.get_or_none(owner_id=user.user_id)

    if shop is None:
        raise HTTPException(status_code=404, detail="Shop not found")

    product_obj = await Product.get_or_none(id=id)

    if product_obj is None:
        raise HTTPException(status_code=404, detail="Product not found")

    if product_obj.shop_id != shop.id:
        raise HTTPException(status_code=404, detail="Product not found")

    await product_obj.delete()

    return None
