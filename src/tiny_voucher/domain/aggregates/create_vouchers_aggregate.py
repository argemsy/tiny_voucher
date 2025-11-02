# Standard Libraries
from typing import Optional

# Own Libraries
from src.tiny_voucher.domain.entities.campaign_entity import EntityCampaign
from src.tiny_voucher.domain.entities.voucher_entity import EntityVoucher


class AggregateCreateVouchers:

    def __init__(
        self,
        campaign: EntityCampaign,
        vouchers: Optional[list[EntityVoucher]] = None,
    ):
        self.campaign = campaign
        self.vouchers = vouchers or []
