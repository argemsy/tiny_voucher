# Third-party Libraries
import structlog

# Own Libraries
from src.tiny_voucher.domain.entities.campaign_entity import EntityCampaign
from src.tiny_voucher.domain.repositories.base_repository import _EntityT
from src.tiny_voucher.domain.services.campaign_service import CampaignService
from src.tiny_voucher.models.audil_log import AuditLogUpdateField
from src.tiny_voucher.shared.exceptions import (
    CampaignServiceExceptionError,
    DomainExceptionError,
    InstanceExistsExceptionError,
)

logger = structlog.getLogger(__name__)


class CampaignServiceImpl(CampaignService[EntityCampaign]):

    async def get_campaign_by_id_admin(self, campaign_pk: str) -> _EntityT:
        try:
            return await self._repository.get_instance(pk=campaign_pk)
        except DomainExceptionError as exp:
            raise CampaignServiceExceptionError(str(exp)) from exp

    async def create_campaign_admin(
        self,
        entity: EntityCampaign,
    ) -> EntityCampaign:
        log_tag = f"{self._cls_name} create_campaign_admin"
        logger.debug(f"***{log_tag}*** Start")
        try:
            if await self._repository.get_instance(  # type: ignore
                name=entity.name
            ):
                raise InstanceExistsExceptionError(
                    f"Campaign with name={entity.name}, was Found."
                )
            return await self._repository.save(entity=entity)  # type: ignore
        except DomainExceptionError as exp:
            raise CampaignServiceExceptionError(str(exp)) from exp

    async def get_diff_with_old_instance(
        self, old_entity: EntityCampaign
    ) -> list[AuditLogUpdateField]:
        candidate_to_change_fields = {
            "total_vouchers",
            "name",
            "discount_type",
            "discount_value",
            "start_date",
            "end_date",
            "description",
            "is_active",
        }
        current_entity = await self._repository.get_instance(pk=old_entity.id)
        update_fields = []

        for field in candidate_to_change_fields:
            previous_value = getattr(old_entity, field, None)
            if previous_value != (
                current_value := getattr(current_entity, field, None)
            ):
                update_fields.append(
                    AuditLogUpdateField(
                        field=field,
                        changes={
                            "previous_value": previous_value,
                            "current_value": current_value,
                        },
                    )
                )
        return update_fields
