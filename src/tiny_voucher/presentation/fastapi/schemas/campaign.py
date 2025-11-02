# Standard Libraries
from datetime import datetime
from typing import Optional

# Third-party Libraries
from pydantic import BaseModel

# Own Libraries
from src.tiny_voucher.domain.entities.campaign_entity import EntityCampaign
from src.tiny_voucher.shared.enums import DiscountTypeEnum


class PrivateCampaignSchema(BaseModel):
    id: str
    name: str
    discount_type: DiscountTypeEnum
    discount_value: float = 0
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime
    total_vouchers: Optional[int] = 0

    @classmethod
    def from_entity(cls, entity: EntityCampaign):
        return cls(
            id=str(entity.id),
            name=entity.name,
            discount_type=entity.discount_type,
            discount_value=entity.discount_value,
            description=entity.description,
            start_date=entity.start_date,
            end_date=entity.end_date,
            total_vouchers=entity.total_vouchers,
        )
