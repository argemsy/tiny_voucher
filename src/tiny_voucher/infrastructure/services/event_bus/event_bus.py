# Standard Libraries
import asyncio
from typing import Any, Callable

# Third-party Libraries
import structlog

# Own Libraries
from src.tiny_voucher.shared.enums import EventBusTopicEnum

logger = structlog.getLogger(__name__)


class EventBus:
    """Base class for both synchronous and asynchronous event buses.

    Provides a foundational mechanism for registering and dispatching event
    handlers. Concrete implementations (sync/async) must define their own
    `publish` logic.
    """

    def __init__(self):
        self._handlers: dict[EventBusTopicEnum, list[Callable[..., Any]]] = {}  # type: ignore

    def register(
        self, topic: EventBusTopicEnum, handler: Callable[..., Any]
    ) -> None:
        """Register a handler function or coroutine for a specific topic.

        Associates one or multiple handler functions with an event topic.
        If no handlers exist for the topic, initializes a new handler list.

        Args:
            topic (EventBusTopicEnum): Enum value identifying the event channel.
            handler (Callable[..., Any]): Function or coroutine that processes the event.
        """
        if topic not in self._handlers:
            self._handlers[topic] = []

        self._handlers[topic].append(handler)

    def _fetch_event_handlers(
        self, topic: EventBusTopicEnum
    ) -> list[Callable[..., Any]]:
        """Return all handlers registered for a given topic.

        Returns a list of handlers associated with the provided topic.
        Logs a debug message if no handlers are found.

        Args:
            topic (EventBusTopicEnum): The event topic.

        Returns:
            list[Callable[..., Any]]: List of handler functions or coroutines.
        """
        handlers = self._handlers.get(topic, [])
        if not handlers:
            logger.debug(f"No handlers registered for topic {topic.value}")
        return handlers


class AsyncEventBus(EventBus):
    """Asynchronous event bus implementation.

    Dispatches events concurrently using `asyncio.gather`.
    Ideal for FastAPI, background workers, or async-driven services.
    """

    async def publish(self, event: Any):
        """Publish an event asynchronously to all registered handlers.

        Dispatches the given event concurrently to every handler registered
        under its topic.

        Args:
            event (Any): Event instance with an attribute `topic` of type `EventBusTopicEnum`.
        """
        handlers = self._fetch_event_handlers(topic=event.topic)
        await asyncio.gather(*(handler(event) for handler in handlers))

        logger.debug(
            "Publishing async event",
            event_topic=event.topic.value,
            handler_count=len(handlers),
        )


class SyncEventBus(EventBus):
    """Synchronous event bus implementation.

    Publishes events sequentially in a blocking manner.
    Suitable for command-line tools or test environments.
    """

    def publish(self, event: Any):
        """Publish an event synchronously to all registered handlers.

        Invokes each registered handler for the given topic sequentially.
        Errors in individual handlers are logged but do not stop execution.

        Args:
            event (Any): Event instance with an attribute `topic` of type `EventBusTopicEnum`.
        """
        if not (handlers := self._fetch_event_handlers(topic=event.topic)):
            return None

        for handler in handlers:
            try:
                handler(event)
            except Exception as exp:
                logger.error(
                    f"Error executing sync handler. "
                    f"Topic: {event.topic.value}, "
                    f"Handler: {handler.__name__}. {exp!r}"
                )

        logger.debug(
            "Publishing sync event",
            event_topic=event.topic.value,
            handler_count=len(handlers),
        )


class EventBusFactory:
    """Factory for creating event bus instances.

    Provides static constructors for both synchronous and asynchronous
    event buses.
    """

    @staticmethod
    def sync() -> SyncEventBus:
        """Create a synchronous event bus instance.

        Returns:
            SyncEventBus: A new synchronous bus instance.
        """
        return SyncEventBus()

    @staticmethod
    def async_() -> AsyncEventBus:
        """Create an asynchronous event bus instance.

        Returns:
            AsyncEventBus: A new asynchronous bus instance.
        """
        return AsyncEventBus()
