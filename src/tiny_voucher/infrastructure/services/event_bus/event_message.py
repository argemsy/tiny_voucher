# Standard Libraries
from typing import Generic

# Own Libraries
from src.tiny_voucher.domain.aggregates.create_vouchers_aggregate import (
    AggregateCreateVouchers,
)
from src.tiny_voucher.domain.entities.campaign_entity import EntityCampaign
from src.tiny_voucher.domain.repositories.base_repository import _EntityT
from src.tiny_voucher.shared.enums import (
    AuditLogActionTypeEnum,
    AuditLogSourceTypeEnum,
    EventBusTopicEnum,
)


class EventBusTopicMessage(Generic[_EntityT]):
    __slots__ = (
        "operation_id",
        "action",
        "source",
        "created_by_id",
        "entity",
        "topic",
    )

    def __init__(
        self,
        operation_id: str,
        action: AuditLogActionTypeEnum,
        source: AuditLogSourceTypeEnum,
        created_by_id: int,
        topic: EventBusTopicEnum,
        entity: _EntityT,
    ):
        self.operation_id = operation_id
        self.action = action
        self.source = source
        self.created_by_id = created_by_id
        self.topic = topic
        self.entity = entity


CreateCampaignTopicMessage = EventBusTopicMessage[EntityCampaign]

CreateVouchersTopicMessage = EventBusTopicMessage[AggregateCreateVouchers]
