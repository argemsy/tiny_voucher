# Standard Libraries
from datetime import datetime
from typing import Optional

# Third-party Libraries
from pydantic import BaseModel


class PrivateVoucherSchema(BaseModel):
    id: str
    code: str
    is_redeemed: bool
    redeemed_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None

    @classmethod
    def from_entity(cls, entity):
        return cls(
            id=str(entity.id),
            code=entity.code,
            is_redeemed=entity.is_redeemed,
            redeemed_at=entity.redeemed_at,
            expires_at=entity.expires_at,
        )
