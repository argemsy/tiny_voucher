# Standard Libraries
import uuid

# Third-party Libraries
import structlog
from django.db import models
from django.utils import timezone

# Own Libraries
from src.tiny_voucher.models.base_model import (
    AuditModel,
    SoftDeleteModel,
)

logger = structlog.getLogger(__name__)


class VoucherModel(AuditModel, SoftDeleteModel):
    id = models.UUIDField(
        primary_key=True, editable=False, default=uuid.uuid4, unique=True
    )
    campaign = models.ForeignKey(
        "CampaignModel", on_delete=models.CASCADE, related_name="vouchers"
    )
    code = models.CharField(max_length=50, unique=True, db_index=True)
    is_redeemed = models.BooleanField(default=False)
    redeemed_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.code}"

    def is_expired(self) -> bool:
        """Check if voucher has expired. / Verifica si el cupón expiró."""
        return bool(self.expires_at and timezone.now() > self.expires_at)

    def can_be_redeemed(self) -> bool:
        """
        Check if voucher is valid for redemption.
        """
        return (
            not self.is_redeemed
            and not self.is_expired()
            and self.campaign.is_active
            and not self.campaign.is_expired()
        )

    class Meta:
        db_table = "voucher"
        ordering = ["-created_at", "-id"]
