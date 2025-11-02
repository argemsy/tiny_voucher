# Own Libraries
from src.tiny_voucher.domain.aggregates.create_vouchers_aggregate import (
    AggregateCreateVouchers,
)
from src.tiny_voucher.domain.entities.audit_log_entity import EntityAuditLog
from src.tiny_voucher.domain.entities.voucher_entity import EntityVoucher
from src.tiny_voucher.domain.repositories.audit_log_repository import (
    AuditLogRepository,
)
from src.tiny_voucher.domain.repositories.base_repository import (
    _EntityT,
    _ModelT,
)
from src.tiny_voucher.infrastructure.services.event_bus.event_message import (
    CreateVouchersTopicMessage,
)
from src.tiny_voucher.shared.enums import AuditLogObjectTypeEnum


class AuditLogRegisterCreateVouchersUseCase:
    def __init__(self, repository: AuditLogRepository[_ModelT, _EntityT]):
        self._repository = repository

    async def execute(self, event: CreateVouchersTopicMessage):
        event_entity: AggregateCreateVouchers = event.entity
        vouchers: list[EntityVoucher] = event_entity.vouchers

        vouchers_to_save = [
            EntityAuditLog(
                object_id=str(voucher.id),
                object_type=AuditLogObjectTypeEnum.CAMPAIGN,
                object_repr=f"<VoucherModel> {voucher.code}",
                action_type=event.action,
                source=event.source,
                description=(
                    f"Registro de voucher {voucher.code} [{voucher.id}] "
                    f"OperationID[{event.operation_id}]"
                ),
                created_by=event.created_by_id,
                created_at=voucher.created_at,
            )
            for voucher in vouchers
        ]

        await self._repository.bulk_save_instances(entities=vouchers_to_save)  # type: ignore
