import phonenumbers
from pydantic import BaseModel, field_validator


class ShopUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    mobile: str | None = None
    address: str | None = None
    is_physical: bool | None = None
    category_id: str | None = None

    @field_validator("name")
    def validate_name(cls, value: str) -> str:
        if value is not None and value == "":
            raise ValueError("Name can not be empty")
        return value

    @field_validator("mobile")
    def validate_mobile(cls, value: str) -> str:
        try:
            phone_number = phonenumbers.parse(value, "IR")
            # Check if the phone number is valid
            if not phonenumbers.is_valid_number(phone_number):
                raise ValueError("Invalid phone number")
        except phonenumbers.phonenumberutil.NumberParseException:
            raise ValueError("Invalid phone number format")
        return value

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Shop name",
                    "description": "Shop description",
                    "mobile": "09301111111",
                    "address": "Shop address",
                    "is_physical": True,
                    "category_id": "01F8MECHZX3TBDSZ7XRADM79XV",
                }
            ]
        }
    }
