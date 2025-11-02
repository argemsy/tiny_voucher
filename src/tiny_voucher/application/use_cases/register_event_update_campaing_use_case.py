# Own Libraries
from src.tiny_voucher.domain.aggregates.create_vouchers_aggregate import (
    AggregateCreateVouchers,
)
from src.tiny_voucher.domain.entities.audit_log_entity import EntityAuditLog
from src.tiny_voucher.domain.entities.campaign_entity import EntityCampaign
from src.tiny_voucher.infrastructure.repositories.django.audit_log_repository_impl import (
    DjangoAuditLogRepositoryImpl,
)
from src.tiny_voucher.infrastructure.services.domain.campaign_service_impl import (
    CampaignServiceImpl,
)
from src.tiny_voucher.infrastructure.services.event_bus.event_message import (
    CreateVouchersTopicMessage,
)
from src.tiny_voucher.models.audil_log import (
    AuditLogMetadata,
)
from src.tiny_voucher.shared.enums import (
    AuditLogActionTypeEnum,
    AuditLogObjectTypeEnum,
    AuditLogSourceTypeEnum,
)


class AuditLogRegisterUpdateCampaignUseCase:
    def __init__(
        self,
        service: CampaignServiceImpl,
        repository: DjangoAuditLogRepositoryImpl,
    ):
        self._service = service
        self._repository = repository

    async def execute(self, event: CreateVouchersTopicMessage) -> None:
        aggregate: AggregateCreateVouchers = event.entity
        old_campaign: EntityCampaign = aggregate.campaign

        first_voucher = aggregate.vouchers[0]

        if not (
            update_fields := await self._service.get_diff_with_old_instance(
                old_entity=old_campaign
            )
        ):
            return None

        audit_log_entity = EntityAuditLog(
            object_id=old_campaign.id,
            object_type=AuditLogObjectTypeEnum.CAMPAIGN,
            object_repr=f"<Campaign> {old_campaign.name}",
            action_type=AuditLogActionTypeEnum.CHANGE,
            source=AuditLogSourceTypeEnum.API,
            created_by=event.created_by_id,
            created_at=first_voucher.created_at,
            description=f"Se ha editado el CampaignModel [{old_campaign.id}]",
            metadata=AuditLogMetadata(update_fields=update_fields).dict(),
        )
        _ = await self._repository.save(entity=audit_log_entity)
        return None
