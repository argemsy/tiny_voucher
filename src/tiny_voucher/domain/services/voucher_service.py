# Standard Libraries
from abc import ABC, abstractmethod
from typing import Generic

# Own Libraries
from src.tiny_voucher.domain.repositories.base_repository import (
    _EntityT,
    _ModelT,
)
from src.tiny_voucher.domain.repositories.voucher_repository import (
    VoucherRepository,
)


class VoucherService(ABC, Generic[_EntityT]):
    def __init__(self, repository: VoucherRepository[_ModelT, _EntityT]):
        self._repository = repository
        self._cls_name = self.__class__.__name__

    @abstractmethod
    async def get_voucher_admin(
        self,
        entity: _EntityT,
    ) -> _EntityT:
        pass

    @abstractmethod
    async def create_vouchers_admin(
        self,
        vouchers: list[_EntityT],
    ):
        pass
