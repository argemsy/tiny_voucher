# Standard Libraries

# Own Libraries
from src.tiny_voucher.domain.entities.audit_log_entity import EntityAuditLog
from src.tiny_voucher.domain.entities.campaign_entity import EntityCampaign
from src.tiny_voucher.domain.repositories.audit_log_repository import (
    AuditLogRepository,
)
from src.tiny_voucher.domain.repositories.base_repository import (
    _EntityT,
    _ModelT,
)
from src.tiny_voucher.infrastructure.services.event_bus.event_message import (
    CreateCampaignTopicMessage,
)
from src.tiny_voucher.shared.enums import AuditLogObjectTypeEnum


class AuditLogRegisterCreateCampaignUseCase:
    def __init__(self, repository: AuditLogRepository[_ModelT, _EntityT]):
        self._repository = repository

    async def execute(self, event: CreateCampaignTopicMessage):
        event_entity: EntityCampaign = event.entity
        entity_to_save = EntityAuditLog(
            object_id=str(event_entity.id),
            object_type=AuditLogObjectTypeEnum.CAMPAIGN,
            object_repr=f"<CampaignModel> {event_entity.name}",
            action_type=event.action,
            source=event.source,
            description=f"Registro de campaña {event_entity.name} [{event_entity.id}]",
            created_by=event.created_by_id,
            created_at=event_entity.created_at,
        )
        await self._repository.save(entity=entity_to_save)  # type: ignore
