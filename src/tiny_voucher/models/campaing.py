# Standard Libraries
import uuid

# Third-party Libraries
import structlog
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

# Own Libraries
from src.tiny_voucher.models.base_model import AuditModel, SoftDeleteModel
from src.tiny_voucher.shared.enums import DiscountTypeEnum

logger = structlog.getLogger(__name__)


class CampaignModel(AuditModel, SoftDeleteModel):
    id = models.UUIDField(
        editable=False, primary_key=True, unique=True, default=uuid.uuid4
    )
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True, null=True)
    discount_type = models.CharField(
        max_length=20, choices=DiscountTypeEnum.choices()
    )
    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Percentage (0–100) or fixed value, depending on discount_type.",
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    total_vouchers = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return f"{self.name}"

    def is_expired(self) -> bool:
        """Check if campaign has expired. / Verifica si la campaña expiró."""
        return timezone.now() > self.end_date

    def is_started(self) -> bool:
        """Check if campaign has started. / Verifica si la campaña ya inició."""
        return timezone.now() >= self.start_date

    # def can_generate_more_vouchers(self) -> bool:
    #     """
    #     Check if more vouchers can be created based on total_vouchers limit.
    #     Verifica si aún se pueden generar más cupones según el límite definido.
    #     """
    #     from vouchers.models import \
    #         Voucher  # local import to avoid circular dependency
    #
    #     current_count = Voucher.objects.filter(campaign=self).count()
    #     return current_count < self.total_vouchers

    class Meta:
        db_table = "campaign"
        ordering = ["-created_at", "-id"]
