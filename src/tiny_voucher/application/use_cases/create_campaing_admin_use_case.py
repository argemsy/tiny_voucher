# Own Libraries
from src.tiny_voucher.application.dtos.create_campaign_dto import (
    CreateCampaignDTO,
)
from src.tiny_voucher.domain.entities.campaign_entity import EntityCampaign
from src.tiny_voucher.infrastructure.services.domain.campaign_service_impl import (
    CampaignServiceImpl,
)
from src.tiny_voucher.shared.exceptions import (
    CampaignServiceExceptionError,
    DomainExceptionError,
)


class CreateCampaignAdminUseCase:
    def __init__(self, service: CampaignServiceImpl):
        self._service = service

    async def execute(self, dto: CreateCampaignDTO):
        try:
            _entity = EntityCampaign(
                name=dto.name,
                discount_type=dto.discount_type,
                discount_value=dto.discount_value,
                start_date=dto.start_date,
                end_date=dto.end_date,
                description=dto.description,
            )
            return await self._service.create_campaign_admin(entity=_entity)
        except CampaignServiceExceptionError as exp:
            raise DomainExceptionError(str(exp)) from exp
