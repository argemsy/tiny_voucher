# Third-party Libraries
import structlog

# Own Libraries
from src.tiny_voucher.domain.entities.voucher_entity import EntityVoucher
from src.tiny_voucher.infrastructure.services.domain.voucher_service_impl import (
    VoucherServiceImpl,
)
from src.tiny_voucher.shared.exceptions import (
    DomainExceptionError,
    VoucherServiceExceptionError,
)

logger = structlog.getLogger(__name__)


class GetVoucherAdminUseCase:
    def __init__(self, service: VoucherServiceImpl):
        self._service = service

    async def execute(self, voucher_pk: str) -> EntityVoucher:
        try:
            _entity = EntityVoucher(id=voucher_pk)
            return await self._service.get_voucher_admin(entity=_entity)
        except VoucherServiceExceptionError as exp:
            raise DomainExceptionError(str(exp)) from exp
