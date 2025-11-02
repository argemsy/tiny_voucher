# Standard Libraries
from datetime import datetime
from typing import Optional

# Third-party Libraries
from pydantic import BaseModel

# Own Libraries
from src.tiny_voucher.shared.enums import DiscountTypeEnum


class CreateCampaignDTO(BaseModel):
    name: str
    discount_type: DiscountTypeEnum
    discount_value: float
    start_date: datetime
    end_date: datetime
    description: Optional[str] = None
