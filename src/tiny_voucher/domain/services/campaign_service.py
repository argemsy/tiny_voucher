# Standard Libraries
from abc import ABC, abstractmethod
from typing import Generic

# Own Libraries
from src.tiny_voucher.domain.repositories.base_repository import (
    _EntityT,
    _ModelT,
)
from src.tiny_voucher.domain.repositories.campaign_repository import (
    CampaignRepository,
)
from src.tiny_voucher.models.audil_log import AuditLogUpdateField


class CampaignService(ABC, Generic[_EntityT]):
    def __init__(self, repository: CampaignRepository[_ModelT, _EntityT]):
        self._repository = repository
        self._cls_name = self.__class__.__name__

    @abstractmethod
    async def get_campaign_by_id_admin(self, campaign_pk: str) -> _EntityT:
        pass

    @abstractmethod
    async def create_campaign_admin(
        self,
        entity: _EntityT,
    ) -> _EntityT:
        pass

    @abstractmethod
    async def get_diff_with_old_instance(
        self, old_entity: _EntityT
    ) -> list[AuditLogUpdateField]:
        pass
