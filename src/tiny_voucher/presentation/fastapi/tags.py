# Own Libraries
from src.tiny_voucher.shared.enums import ResourceScopeEnum
from src.tiny_voucher.shared.utils.tags import ExternalDocs, MetadataTag

voucher_admin_tag = MetadataTag(
    name="Voucher Admin",
    description="Detalle del voucher desde la sección del administrador",
    version=1,
    scope=ResourceScopeEnum.ADMIN,
    external_docs=ExternalDocs(
        description="Fake Url",
        url="https://as.com",
    ),
)

create_vouchers_admin_tag = MetadataTag(
    name="Create Vouchers Admin",
    description="Crea un conjunto de vouchers de manera masiva para una campaña desde la sección del administrador",
    version=1,
    scope=ResourceScopeEnum.ADMIN,
    external_docs=ExternalDocs(
        description="Fake Url",
        url="https://as.com",
    ),
)

create_campaign_admin_tag = MetadataTag(
    name="Create Campaign Admin",
    description=(
        "Creación de una campaña desde la sección del administrador. Este servicio "
        "permite registrar a traves de un bus de eventos el historial de "
        "cambios para una campaña."
    ),
    version=1,
    scope=ResourceScopeEnum.ADMIN,
    external_docs=ExternalDocs(
        description="Fake Url",
        url="https://as.com",
    ),
)


VOUCHER_TAGS = [
    voucher_admin_tag,
    create_campaign_admin_tag,
    create_vouchers_admin_tag,
]
