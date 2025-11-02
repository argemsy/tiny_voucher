# Own Libraries
from src.tiny_voucher.infrastructure.services.event_bus.event_bus import (
    EventBusFactory,
)
from src.tiny_voucher.infrastructure.services.event_bus.handlers import (
    AsyncEventBusHandler,
)
from src.tiny_voucher.shared.enums import EventBusTopicEnum

# Sync Event Bus
sync_bus = EventBusFactory.sync()


# Async Event Bus
async_bus = EventBusFactory.async_()
async_bus.register(
    topic=EventBusTopicEnum.CREATE_CAMPAIGN,
    handler=AsyncEventBusHandler.register_create_campaign_handler,
)
async_bus.register(
    topic=EventBusTopicEnum.CREATE_VOUCHERS,
    handler=AsyncEventBusHandler.register_create_vouchers_handler,
)
async_bus.register(
    topic=EventBusTopicEnum.CREATE_VOUCHERS,
    handler=AsyncEventBusHandler.register_update_total_vouchers_in_campaign_handler,
)
async_bus.register(
    topic=EventBusTopicEnum.UPDATE_CAMPAIGN,
    handler=AsyncEventBusHandler.register_update_campaign_handler,
)
