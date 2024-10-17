from tortoise import fields
from tortoise.exceptions import ValidationError

from .base import BaseModel


class Product(BaseModel):
    """Model to represent products."""

    shop = fields.ForeignKeyField(
        "models.Shop", related_name="products", on_delete=fields.CASCADE
    )

    name = fields.CharField(max_length=255, index=True)

    description = fields.TextField(null=True)

    price = fields.IntField()

    is_active = fields.BooleanField(default=True)

    class Meta:
        table = "products"

    def __str__(self):
        return self.name

    async def save(self, *args, **kwargs):
        if self.price <= 0:
            raise ValidationError("Price must be a positive integer")
        await super().save(*args, **kwargs)
