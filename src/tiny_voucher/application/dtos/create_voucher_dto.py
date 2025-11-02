# Standard Libraries
from datetime import datetime

# Third-party Libraries
from pydantic import BaseModel


class VoucherDTO(BaseModel):
    expires_at: datetime
    code: str


class CreateVoucherAdminDTO(BaseModel):
    campaign_id: str
    voucher_codes: list[VoucherDTO]
