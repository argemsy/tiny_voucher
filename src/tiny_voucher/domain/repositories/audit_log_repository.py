# Standard Libraries
from abc import ABC, abstractmethod

# Own Libraries
from src.tiny_voucher.domain.repositories.base_repository import (
    BaseRepository,
    _EntityT,
    _ModelT,
)


class AuditLogRepository(BaseRepository[_ModelT, _EntityT], ABC):
    @abstractmethod
    def save(self, entity: _EntityT) -> _EntityT:
        pass

    @abstractmethod
    def bulk_save_instances(self, entities: list[_EntityT]) -> list[_EntityT]:
        pass
