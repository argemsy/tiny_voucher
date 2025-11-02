# Third-party Libraries

# Third-party Libraries
import structlog

# Own Libraries
from src.tiny_voucher.domain.entities.audit_log_entity import EntityAuditLog
from src.tiny_voucher.domain.repositories.audit_log_repository import (
    AuditLogRepository,
)
from src.tiny_voucher.domain.repositories.base_repository import _EntityT
from src.tiny_voucher.models import AuditLogModel
from src.tiny_voucher.shared.utils.database import async_database

logger = structlog.getLogger(__name__)


class DjangoAuditLogRepositoryImpl(
    AuditLogRepository[AuditLogModel, EntityAuditLog]
):
    model_cls = AuditLogModel
    entity_cls = EntityAuditLog

    @async_database()
    def bulk_save_instances(self, entities: list[_EntityT]) -> list[_EntityT]:
        try:
            model_cls = self.get_model_cls()
            to_create = [
                model_cls(
                    object_id=entity.object_id,
                    object_type=entity.object_type.value,
                    object_repr=entity.object_repr,
                    action_type=entity.action_type.value,
                    source=entity.source.value,
                    description=entity.description,
                    created_by=entity.created_by,
                    created_at=entity.created_at,
                    metadata=entity.metadata,
                )
                for entity in entities
            ]

            instances = model_cls.objects.bulk_create(to_create)
            _entity_cls = self.get_entity_cls()

            return [
                _entity_cls.from_model(instance=instance)
                for instance in instances
            ]
        except Exception as exp:
            logger.error(
                f"***{self.__class__.__name__} save*** InternalError {exp!r}"
            )
            raise Exception(str(exp)) from exp

    @async_database()
    def save(self, entity: EntityAuditLog) -> EntityAuditLog:
        try:
            model_cls = self.get_model_cls()

            instance = model_cls(
                object_id=entity.object_id,
                object_type=entity.object_type.value,
                object_repr=entity.object_repr,
                action_type=entity.action_type.value,
                source=entity.source.value,
                description=entity.description,
                created_by=entity.created_by,
                created_at=entity.created_at,
                metadata=entity.metadata,
            )
            instance.save()
            _entity_cls = self.get_entity_cls()
            return _entity_cls.from_model(instance=instance)
        except Exception as exp:
            logger.error(
                f"***{self.__class__.__name__} save*** InternalError {exp!r}"
            )
            raise Exception(str(exp)) from exp
