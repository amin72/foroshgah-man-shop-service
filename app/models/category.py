from tortoise import fields

from .base import BaseModel


class Category(BaseModel):
    """Abstract model to represent categories."""

    title = fields.CharField(max_length=200, index=True)
    slug = fields.CharField(max_length=200, index=True)

    image = fields.CharField(max_length=255, null=True)

    is_active = fields.BooleanField(default=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class ShopCategory(Category):
    """Model to represent shop-categories."""

    class Meta:
        table = "shop_categories"
