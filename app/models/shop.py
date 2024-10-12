from tortoise import fields

from .base import BaseModel


class Shop(BaseModel):
    """Model to represent shops."""

    name = fields.CharField(max_length=200, index=True, null=True)
    owner_id = fields.CharField(index=True, max_length=26)

    class Meta:
        table = "shops"

    def __str__(self):
        return self.name
