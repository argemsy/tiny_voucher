from typing import Optional

from pydantic import BaseModel, Field


class GenerateVoucherAdminDTO(BaseModel):
    code: str
    amount: float
    description: Optional[str] = Field(default=None)
    is_active: bool = Field(default=True)
