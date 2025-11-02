# Own Libraries
from src.tiny_voucher.domain.aggregates.create_vouchers_aggregate import (
    AggregateCreateVouchers,
)
from src.tiny_voucher.domain.entities.campaign_entity import EntityCampaign
from src.tiny_voucher.infrastructure.repositories.django.campaign_repository_impl import (
    DjangoCampaignRepositoryImpl,
)
from src.tiny_voucher.infrastructure.services.event_bus.event_message import (
    CreateVouchersTopicMessage,
)


class AuditLogRegisterUpdateTotalVouchersInCampaignUseCase:

    def __init__(self, repository: DjangoCampaignRepositoryImpl):
        self._repository = repository

    async def execute(self, event: CreateVouchersTopicMessage):

        aggregate: AggregateCreateVouchers = event.entity
        entity: EntityCampaign = aggregate.campaign

        new_total_vouchers_value = entity.total_vouchers + len(
            aggregate.vouchers
        )

        _entity = await self._repository.update_instance(
            entity=entity,
            map_changes={"total_vouchers": new_total_vouchers_value},
        )
