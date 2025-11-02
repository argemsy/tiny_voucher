# Standard Libraries
from abc import ABC, abstractmethod
from typing import Optional

# Own Libraries
from src.tiny_voucher.domain.repositories.base_repository import (
    BaseRepository,
    _EntityT,
    _ModelT,
)


class VoucherRepository(BaseRepository[_ModelT, _EntityT], ABC):
    @abstractmethod
    def get_instance(self, entity: _EntityT) -> Optional[_EntityT]:
        pass

    @abstractmethod
    def bulk_save_instances(self, entities: list[_EntityT]) -> list[_EntityT]:
        pass
