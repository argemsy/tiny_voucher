# Standard Libraries
import uuid

# Third-party Libraries
import structlog
from django.db import models

# Own Libraries
from src.tiny_voucher.models.base_model import (
    AuditModel,
    SoftDeleteModel,
)

logger = structlog.getLogger(__name__)


class VoucherRedemptionModel(AuditModel, SoftDeleteModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    voucher = models.OneToOneField(
        "VoucherModel",
        on_delete=models.CASCADE,
        related_name="redemption",
    )
    redeemed_by = models.CharField(
        max_length=150,
        help_text="Identifier of the user or entity that redeemed the voucher.",
    )
    redeemed_at = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.voucher}"

    class Meta:
        db_table = "voucher_redemptions"
        ordering = ["-redeemed_at", "-id"]
