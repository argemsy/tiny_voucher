# Standard Libraries
from typing import Union

# Own Libraries
from src.tiny_voucher.presentation.fastapi.responses.errors import ErrorSchema
from src.tiny_voucher.presentation.fastapi.responses.payloads import (
    CreateCampaignSchemaPayload,
    CreateVouchersSchemaPayload,
    VoucherDetailSchemaPayload,
)

VoucherDetailSchemaFragment = Union[VoucherDetailSchemaPayload, ErrorSchema]

CreateCampaignSchemaFragment = Union[CreateCampaignSchemaPayload, ErrorSchema]

CreateVouchersSchemaFragment = Union[CreateVouchersSchemaPayload, ErrorSchema]
