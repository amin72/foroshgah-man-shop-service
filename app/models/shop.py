from tortoise import fields

from .base import BaseModel


class Shop(BaseModel):
    """Model to represent shops."""

    owner_id = fields.CharField(index=True, max_length=26)

    name = fields.CharField(max_length=200, index=True, null=True)

    description = fields.CharField(max_length=1000, null=True)

    address = fields.CharField(max_length=1000, null=True)

    mobile = fields.CharField(max_length=11, null=True)

    is_physical = fields.BooleanField(default=False)

    category = fields.ForeignKeyField(
        "models.ShopCategory",
        related_name="shops",
        on_delete=fields.SET_NULL,
        null=True,
    )

    class Meta:
        table = "shops"

    def __str__(self):
        return self.name
