# Standard Libraries
from datetime import datetime, timezone
from typing import Any, Optional

# Third-party Libraries
import structlog

# Own Libraries
from src.tiny_voucher.domain.entities.campaign_entity import EntityCampaign
from src.tiny_voucher.domain.repositories.campaign_repository import (
    CampaignRepository,
)
from src.tiny_voucher.models import CampaignModel
from src.tiny_voucher.shared.exceptions import InstanceNotFoundExceptionError
from src.tiny_voucher.shared.utils.database import async_database

logger = structlog.getLogger(__name__)


class DjangoCampaignRepositoryImpl(
    CampaignRepository[CampaignModel, EntityCampaign]
):
    model_cls = CampaignModel
    entity_cls = EntityCampaign

    @async_database()
    def get_instance(
        self, pk: Optional[str] = None, name: Optional[str] = None
    ) -> Optional[EntityCampaign]:
        model_cls = self.get_model_cls()

        filters = {}
        if name:
            filters["name"] = name
        if pk:
            filters["id"] = pk

        queryset = model_cls.objects.filter(**filters)

        if not (instance := queryset.first()):
            return None

        if instance.is_deleted:
            return None

        entity_cls = self.get_entity_cls()

        return entity_cls.from_model(instance=instance)

    @async_database()
    def save(self, entity: EntityCampaign) -> EntityCampaign:
        try:
            model_cls = self.get_model_cls()
            instance = model_cls(
                name=entity.name,
                description=entity.description,
                discount_type=entity.discount_type.value,
                discount_value=entity.discount_value,
                start_date=entity.start_date,
                end_date=entity.end_date,
                total_vouchers=entity.total_vouchers,
                is_active=entity.is_active,
            )
            instance.save()
            _entity = self.get_entity_cls()
            return _entity.from_model(instance=instance)
        except Exception as exp:
            logger.error(
                f"***{self.__class__.__name__} save***, Error {exp!r}",
            )
            raise Exception(str(exp)) from exp

    @async_database()
    def update_instance(
        self, entity: EntityCampaign, map_changes: dict[str, Any]
    ) -> EntityCampaign:

        tz_now = datetime.now(timezone.utc)

        model_cls = self.get_model_cls()
        queryset = model_cls.objects.filter(pk=entity.id, is_deleted=False)
        if not (instance := queryset.first()):
            raise InstanceNotFoundExceptionError(
                f"Campaign with id={entity.id}, not found."
            )

        entity_cls = self.get_entity_cls()

        update_fields = []

        for field, incoming_value in map_changes.items():
            if getattr(instance, field, None) != incoming_value:
                setattr(instance, field, incoming_value)
                update_fields.append(field)

        if update_fields:
            instance.updated_at = tz_now
            update_fields.append("updated_at")
            instance.save(update_fields=update_fields)

        return entity_cls.from_model(instance=instance)
