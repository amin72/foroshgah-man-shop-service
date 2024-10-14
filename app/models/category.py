from tortoise import fields

from .base import BaseModel


class Category(BaseModel):
    """Model to represent categories."""

    title = fields.CharField(max_length=200, index=True)
    slug = fields.CharField(max_length=200, index=True)

    class Meta:
        table = "categories"

    def __str__(self):
        return self.title
