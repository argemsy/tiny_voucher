# Third-party Libraries
import structlog

# Own Libraries
from src.tiny_voucher.application.use_cases.register_event_create_campaign import (
    AuditLogRegisterCreateCampaignUseCase,
)
from src.tiny_voucher.application.use_cases.register_event_create_vouchers_use_case import (
    AuditLogRegisterCreateVouchersUseCase,
)
from src.tiny_voucher.application.use_cases.register_event_total_vouchers_in_campaign_use_case import (
    AuditLogRegisterUpdateTotalVouchersInCampaignUseCase,
)
from src.tiny_voucher.application.use_cases.register_event_update_campaing_use_case import (
    AuditLogRegisterUpdateCampaignUseCase,
)
from src.tiny_voucher.infrastructure.repositories.django.audit_log_repository_impl import (
    DjangoAuditLogRepositoryImpl,
)
from src.tiny_voucher.infrastructure.repositories.django.campaign_repository_impl import (
    DjangoCampaignRepositoryImpl,
)
from src.tiny_voucher.infrastructure.services.domain.campaign_service_impl import (
    CampaignServiceImpl,
)
from src.tiny_voucher.infrastructure.services.event_bus.event_message import (
    CreateCampaignTopicMessage,
    CreateVouchersTopicMessage,
)

logger = structlog.getLogger(__name__)


class AsyncEventBusHandler:
    @staticmethod
    async def register_create_campaign_handler(
        event: CreateCampaignTopicMessage,
    ):
        try:
            use_case = AuditLogRegisterCreateCampaignUseCase(
                repository=DjangoAuditLogRepositoryImpl()
            )
            await use_case.execute(event=event)
        except Exception as exp:
            raise Exception(str(exp)) from exp

    @staticmethod
    async def register_create_vouchers_handler(
        event: CreateVouchersTopicMessage,
    ):
        try:
            use_case = AuditLogRegisterCreateVouchersUseCase(
                repository=DjangoAuditLogRepositoryImpl()
            )
            await use_case.execute(event=event)
        except Exception as exp:
            raise Exception(str(exp)) from exp

    @staticmethod
    async def register_update_total_vouchers_in_campaign_handler(
        event: CreateVouchersTopicMessage,
    ):
        try:
            use_case = AuditLogRegisterUpdateTotalVouchersInCampaignUseCase(
                repository=DjangoCampaignRepositoryImpl()
            )
            await use_case.execute(event=event)

        except Exception as exp:
            raise Exception(str(exp)) from exp

    @staticmethod
    async def register_update_campaign_handler(
        event: CreateVouchersTopicMessage,
    ):
        try:
            use_case = AuditLogRegisterUpdateCampaignUseCase(
                service=CampaignServiceImpl(
                    repository=DjangoCampaignRepositoryImpl()
                ),
                repository=DjangoAuditLogRepositoryImpl(),
            )
            await use_case.execute(event=event)

        except Exception as exp:
            raise Exception(str(exp)) from exp
