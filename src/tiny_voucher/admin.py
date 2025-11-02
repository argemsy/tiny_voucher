# Third-party Libraries
from django.contrib import admin

# Own Libraries
from src.tiny_voucher.models import (
    AuditLogModel,
    CampaignModel,
    VoucherModel,
    VoucherRedemptionModel,
)

for model in [
    AuditLogModel,
    VoucherModel,
    VoucherRedemptionModel,
    CampaignModel,
]:
    admin.site.register(model)
