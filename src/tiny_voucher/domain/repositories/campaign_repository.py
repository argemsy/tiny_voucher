# Standard Libraries
from abc import ABC, abstractmethod
from typing import Any, Optional

# Own Libraries
from src.tiny_voucher.domain.repositories.base_repository import (
    BaseRepository,
    _EntityT,
    _ModelT,
)


class CampaignRepository(BaseRepository[_ModelT, _EntityT], ABC):

    @abstractmethod
    def get_instance(
        self, pk: Optional[str], name: Optional[str]
    ) -> Optional[_EntityT]:
        pass

    @abstractmethod
    def update_instance(
        self, entity: _EntityT, map_changes: dict[str, Any]
    ) -> _EntityT:
        pass

    @abstractmethod
    def save(self, entity: _EntityT) -> _EntityT:
        pass
