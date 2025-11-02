# Third-party Libraries
from pydantic import BaseModel, Field

# Own Libraries
from src.tiny_voucher.presentation.fastapi.schemas.campaign import (
    PrivateCampaignSchema,
)
from src.tiny_voucher.presentation.fastapi.schemas.voucher import (
    PrivateVoucherSchema,
)


class VoucherDetailSchemaPayload(BaseModel):
    voucher: PrivateVoucherSchema


class CreateCampaignSchemaPayload(BaseModel):
    operation_id: str
    campaign: PrivateCampaignSchema


class CreateVouchersSchemaPayload(BaseModel):
    operation_id: str
    campaign: PrivateCampaignSchema
    vouchers: list[PrivateVoucherSchema] = Field(default_factory=list)
