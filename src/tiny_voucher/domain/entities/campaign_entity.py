# Standard Libraries
from datetime import datetime, timezone
from typing import Optional

# Own Libraries
from src.tiny_voucher.shared.enums import DiscountTypeEnum


class EntityCampaign:
    def __init__(
        self,
        name: str,
        discount_type: DiscountTypeEnum,
        discount_value: float,
        start_date: datetime,
        end_date: datetime,
        description: Optional[str] = None,
        id: Optional[str] = None,
        total_vouchers: Optional[int] = 0,
        is_active: Optional[bool] = True,
        created_at: Optional[datetime] = None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.discount_type = discount_type
        self.discount_value = discount_value
        self.start_date = start_date
        self.end_date = end_date
        self.total_vouchers = total_vouchers
        self.is_active = is_active
        self.created_at = created_at or datetime.now(timezone.utc)

    @classmethod
    def from_model(cls, instance):
        return cls(
            id=instance.id,
            name=instance.name,
            description=instance.description,
            discount_type=DiscountTypeEnum[instance.discount_type],
            discount_value=instance.discount_value,
            start_date=instance.start_date,
            end_date=instance.end_date,
            total_vouchers=instance.total_vouchers,
            is_active=instance.is_active,
            created_at=instance.created_at,
        )
