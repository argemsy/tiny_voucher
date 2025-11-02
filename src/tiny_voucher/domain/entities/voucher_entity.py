# Standard Libraries
from datetime import datetime, timezone
from typing import Optional, Self, Union


class EntityVoucher:
    def __init__(
        self,
        campaign_id: Optional[str] = None,
        code: Optional[str] = None,
        id: Optional[str] = None,
        is_redeemed: Optional[bool] = None,
        redeemed_at: Union[datetime, str, None] = None,
        expires_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
    ):
        # self.id = UUIDValueObject(value=id).value
        # self.campaign_id = campaign_id
        # self.code = code
        # self.is_redeemed = is_redeemed or False
        # self.redeemed_at = RedeemedAtVO(value=redeemed_at).value  # type: ignore
        # self.expires_at = ExpiresAtVO(value=expires_at).value
        # self.created_at = created_at or datetime.now(timezone.utc)

        self.id = id
        self.campaign_id = campaign_id
        self.code = code
        self.is_redeemed = is_redeemed or False
        self.redeemed_at = redeemed_at  # type: ignore
        self.expires_at = expires_at
        self.created_at = created_at or datetime.now(timezone.utc)

    @classmethod
    def from_model(cls, instance) -> Self:
        return cls(
            # id=UUIDValueObject(value=instance.id).value,
            # campaign_id=instance.campaign_id,
            # code=instance.code,
            # is_redeemed=instance.is_redeemed,
            # redeemed_at=RedeemedAtVO(
            #     value=instance.redeemed_at,
            # ).value,
            # expires_at=ExpiresAtVO(value=instance.expires_at).value,
            # created_at=instance.created_at,
            id=instance.id,
            campaign_id=instance.campaign_id,
            code=instance.code,
            is_redeemed=instance.is_redeemed,
            redeemed_at=instance.redeemed_at,
            expires_at=instance.expires_at,
            created_at=instance.created_at,
        )
