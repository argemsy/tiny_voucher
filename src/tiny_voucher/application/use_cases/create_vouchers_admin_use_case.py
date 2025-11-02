# Own Libraries
from src.tiny_voucher.application.dtos.create_voucher_dto import (
    CreateVoucherAdminDTO,
)
from src.tiny_voucher.domain.aggregates.create_vouchers_aggregate import (
    AggregateCreateVouchers,
)
from src.tiny_voucher.domain.entities.campaign_entity import EntityCampaign
from src.tiny_voucher.domain.entities.voucher_entity import EntityVoucher
from src.tiny_voucher.infrastructure.services.domain.campaign_service_impl import (
    CampaignServiceImpl,
)
from src.tiny_voucher.infrastructure.services.domain.voucher_service_impl import (
    VoucherServiceImpl,
)
from src.tiny_voucher.shared.exceptions import (
    CampaignServiceExceptionError,
    DomainExceptionError,
    VoucherServiceExceptionError,
)


class CreateVouchersAdminUseCase:
    def __init__(
        self,
        campaign_service: CampaignServiceImpl,
        voucher_service: VoucherServiceImpl,
    ):
        self._campaign_service = campaign_service
        self._voucher_service = voucher_service

    async def execute(
        self, dto: CreateVoucherAdminDTO
    ) -> AggregateCreateVouchers:
        try:
            entity_campaign: EntityCampaign = (
                await self._campaign_service.get_campaign_by_id_admin(
                    campaign_pk=dto.campaign_id,
                )
            )
            entities_voucher: list[EntityVoucher] = (
                await self._voucher_service.create_vouchers_admin(
                    dto=dto,
                )
            )
            return AggregateCreateVouchers(
                campaign=entity_campaign,
                vouchers=entities_voucher,
            )
        except (
            CampaignServiceExceptionError,
            VoucherServiceExceptionError,
        ) as exp:
            raise DomainExceptionError(str(exp)) from exp
