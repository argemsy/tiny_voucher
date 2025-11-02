# Standard Libraries
from typing import Optional

# Third-party Libraries
from pydantic import BaseModel

# Own Libraries
from src.tiny_voucher.shared.enums import ErrorSchemaEnum


class ErrorSchema(BaseModel):
    operation_id: str
    type: ErrorSchemaEnum
    message: Optional[str] = None

    class Config:
        use_enum_values = True
