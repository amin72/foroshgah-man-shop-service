import ulid
from tortoise import fields, models


class BaseModel(models.Model):
    id = fields.CharField(
        primary_key=True, max_length=26, default=lambda: str(ulid.new())
    )
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True
