# Third-party Libraries
import structlog
from fastapi import APIRouter, Depends

# Own Libraries
from src.tiny_voucher.application.dtos.create_campaign_dto import (
    CreateCampaignDTO,
)
from src.tiny_voucher.application.dtos.create_voucher_dto import (
    CreateVoucherAdminDTO,
)
from src.tiny_voucher.application.use_cases.create_campaing_admin_use_case import (
    CreateCampaignAdminUseCase,
)
from src.tiny_voucher.application.use_cases.create_vouchers_admin_use_case import (
    CreateVouchersAdminUseCase,
)
from src.tiny_voucher.application.use_cases.get_voucher_admin_use_case import (
    GetVoucherAdminUseCase,
)
from src.tiny_voucher.domain.aggregates.create_vouchers_aggregate import (
    AggregateCreateVouchers,
)
from src.tiny_voucher.infrastructure.repositories.django.campaign_repository_impl import (
    DjangoCampaignRepositoryImpl,
)
from src.tiny_voucher.infrastructure.repositories.django.voucher_repository_impl import (
    DjangoVoucherRepositoryImpl,
)
from src.tiny_voucher.infrastructure.services.domain.campaign_service_impl import (
    CampaignServiceImpl,
)
from src.tiny_voucher.infrastructure.services.domain.voucher_service_impl import (
    VoucherServiceImpl,
)
from src.tiny_voucher.infrastructure.services.event_bus.event_message import (
    CreateCampaignTopicMessage,
    CreateVouchersTopicMessage,
)
from src.tiny_voucher.infrastructure.services.event_bus.subscriptions import (
    async_bus,
)
from src.tiny_voucher.presentation.fastapi.fragments import (
    CreateCampaignSchemaFragment,
    CreateVouchersSchemaFragment,
    VoucherDetailSchemaFragment,
)
from src.tiny_voucher.presentation.fastapi.inputs import GetVoucherInput
from src.tiny_voucher.presentation.fastapi.responses.error_handler import (
    error_response_handler,
)
from src.tiny_voucher.presentation.fastapi.responses.payloads import (
    CreateCampaignSchemaPayload,
    CreateVouchersSchemaPayload,
    VoucherDetailSchemaPayload,
)
from src.tiny_voucher.presentation.fastapi.schemas.campaign import (
    PrivateCampaignSchema,
)
from src.tiny_voucher.presentation.fastapi.schemas.voucher import (
    PrivateVoucherSchema,
)
from src.tiny_voucher.presentation.fastapi.tags import (
    create_campaign_admin_tag,
    create_vouchers_admin_tag,
    voucher_admin_tag,
)
from src.tiny_voucher.shared.enums import (
    AuditLogActionTypeEnum,
    AuditLogSourceTypeEnum,
    EventBusTopicEnum,
)
from src.tiny_voucher.shared.utils.generator_operation_identifier import (
    get_operation_id,
)

logger = structlog.getLogger(__name__)

voucher_admin_router = APIRouter()


@voucher_admin_router.post(
    "/voucher",
    tags=[voucher_admin_tag.name],
    response_model=VoucherDetailSchemaFragment,
    responses={
        200: {"description": "Success result"},
        400: {"description": "Validation error"},
        500: {"description": "Internal error"},
    },
)
@error_response_handler(path=__name__)
async def get_voucher_admin(input: GetVoucherInput = Depends()):
    use_case = GetVoucherAdminUseCase(
        service=VoucherServiceImpl(repository=DjangoVoucherRepositoryImpl())
    )
    _entity = await use_case.execute(voucher_pk=input.voucher_id)
    return VoucherDetailSchemaPayload(
        voucher=PrivateVoucherSchema.from_entity(entity=_entity),
    )


@voucher_admin_router.post(
    "/create-campaign",
    tags=[create_campaign_admin_tag.name],
    response_model=CreateCampaignSchemaFragment,
    responses={
        200: {"description": "Success result"},
        400: {"description": "Validation error"},
        500: {"description": "Internal error"},
    },
)
@error_response_handler(path=__name__)
async def create_campaign_admin(input: CreateCampaignDTO):
    operation_id = get_operation_id()
    use_case = CreateCampaignAdminUseCase(
        service=CampaignServiceImpl(repository=DjangoCampaignRepositoryImpl())
    )
    _entity = await use_case.execute(dto=input)

    # trigger domain event
    event_message = CreateCampaignTopicMessage(
        operation_id=operation_id,
        action=AuditLogActionTypeEnum.ADDITION,
        source=AuditLogSourceTypeEnum.API,
        created_by_id=1,
        topic=EventBusTopicEnum.CREATE_CAMPAIGN,
        entity=_entity,
    )
    await async_bus.publish(event=event_message)

    return CreateCampaignSchemaPayload(
        operation_id=operation_id,
        campaign=PrivateCampaignSchema.from_entity(entity=_entity),
    )


@voucher_admin_router.post(
    "/create-vouchers",
    tags=[create_vouchers_admin_tag.name],
    response_model=CreateVouchersSchemaFragment,
    responses={
        200: {"description": "Success result"},
        400: {"description": "Validation error"},
        500: {"description": "Internal error"},
    },
)
@error_response_handler(path=__name__)
async def create_vouchers_admin(input: CreateVoucherAdminDTO):
    operation_id = get_operation_id()
    use_case = CreateVouchersAdminUseCase(
        campaign_service=CampaignServiceImpl(
            repository=DjangoCampaignRepositoryImpl()
        ),
        voucher_service=VoucherServiceImpl(
            repository=DjangoVoucherRepositoryImpl()
        ),
    )
    aggregate: AggregateCreateVouchers = await use_case.execute(dto=input)

    for topic in [
        EventBusTopicEnum.CREATE_VOUCHERS,
        EventBusTopicEnum.UPDATE_CAMPAIGN,
    ]:
        event_message = CreateVouchersTopicMessage(
            operation_id=operation_id,
            action=AuditLogActionTypeEnum.ADDITION,
            source=AuditLogSourceTypeEnum.API,
            created_by_id=1,
            topic=topic,
            entity=aggregate,
        )
        await async_bus.publish(event=event_message)

    return CreateVouchersSchemaPayload(
        operation_id=operation_id,
        campaign=PrivateCampaignSchema.from_entity(entity=aggregate.campaign),
        vouchers=[
            PrivateVoucherSchema.from_entity(entity=voucher_entity)
            for voucher_entity in aggregate.vouchers
        ],
    )
