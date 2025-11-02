# Standard Libraries

# Third-party Libraries
import structlog

# Own Libraries
from src.tiny_voucher.application.dtos.create_voucher_dto import (
    CreateVoucherAdminDTO,
)
from src.tiny_voucher.domain.entities.voucher_entity import EntityVoucher
from src.tiny_voucher.domain.services.voucher_service import VoucherService
from src.tiny_voucher.shared.exceptions import (
    DomainExceptionError,
    InstanceNotFoundExceptionError,
    VoucherServiceExceptionError,
)

logger = structlog.getLogger(__name__)


class VoucherServiceImpl(VoucherService[EntityVoucher]):

    async def create_vouchers_admin(
        self, dto: CreateVoucherAdminDTO
    ) -> list[EntityVoucher]:
        log_tag = f"{self._cls_name} get_voucher_admin"
        logger.debug(f"***{log_tag}*** Start")
        try:
            vouchers = [
                EntityVoucher(
                    campaign_id=dto.campaign_id,
                    code=voucher.code,
                    expires_at=voucher.expires_at,
                )
                for voucher in dto.voucher_codes
            ]

            return await self._repository.bulk_save_instances(entities=vouchers)  # type: ignore
        except DomainExceptionError as exp:
            raise VoucherServiceExceptionError(str(exp)) from exp

    async def get_voucher_admin(
        self,
        entity: EntityVoucher,
    ) -> EntityVoucher:
        log_tag = f"{self._cls_name} get_voucher_admin"
        logger.debug(f"***{log_tag}*** Start")
        try:
            if not (
                _entity := await self._repository.get_instance(entity=entity)  # type: ignore
            ):
                raise InstanceNotFoundExceptionError(
                    f"Voucher with id={entity.id}, Not Found."
                )
            return _entity
        except DomainExceptionError as exp:
            raise VoucherServiceExceptionError(str(exp)) from exp
