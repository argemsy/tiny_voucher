# Third-party Libraries
from pydantic import BaseModel, Field


class GetVoucherInput(BaseModel):
    voucher_id: str = Field(alias="id")
