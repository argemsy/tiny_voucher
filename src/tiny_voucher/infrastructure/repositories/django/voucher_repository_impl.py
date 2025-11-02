# Standard Libraries
from typing import Optional

# Own Libraries
from src.tiny_voucher.domain.entities.voucher_entity import EntityVoucher
from src.tiny_voucher.domain.repositories.voucher_repository import (
    VoucherRepository,
)
from src.tiny_voucher.models import VoucherModel
from src.tiny_voucher.shared.utils.database import async_database


class DjangoVoucherRepositoryImpl(
    VoucherRepository[VoucherModel, EntityVoucher]
):
    model_cls = VoucherModel
    entity_cls = EntityVoucher

    @async_database()
    def bulk_save_instances(
        self, entities: list[EntityVoucher]
    ) -> list[EntityVoucher]:
        unique_codes = set()
        model_cls = self.get_model_cls()

        if not (
            objs := [
                model_cls(
                    code=entity.code,
                    campaign_id=entity.campaign_id,
                    expires_at=entity.expires_at,
                )
                for entity in entities
                if (
                    entity.code not in unique_codes
                    and not unique_codes.add(entity.code)
                )
            ]
        ):
            return []

        instances = model_cls.objects.bulk_create(objs)
        entity_cls = self.get_entity_cls()
        return [
            entity_cls.from_model(instance=instance) for instance in instances
        ]

    @async_database()
    def get_instance(self, entity: EntityVoucher) -> Optional[EntityVoucher]:
        model_cls = self.get_model_cls()

        queryset = model_cls.objects.filter(id=entity.id, is_deleted=False)
        if not (instance := queryset.first()):
            return None

        entity_cls = self.get_entity_cls()
        return entity_cls.from_model(instance=instance)
