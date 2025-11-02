# Standard Libraries
from datetime import datetime, timezone
from typing import Optional

# Own Libraries
from src.tiny_voucher.shared.exceptions import (
    DomainExceptionError,
    ValueObjectExceptionError,
)


class RedeemedAtVO:
    def __init__(self, value: Optional[datetime] = None):
        self._cls_name = self.__class__.__name__
        self._value = value

        self.check_value()

    @property
    def value(self):
        return self._value

    def _validate_value_gt(self, incoming_time: datetime) -> None:
        if incoming_time > datetime.now(timezone.utc):
            raise ValueObjectExceptionError(
                f"Invalid value in {self._cls_name}. "
                f"Value={incoming_time.isoformat()} cannot be greater than now."
            )

    def check_value(self) -> None:
        """Validates and normalizes the internal datetime value."""
        if not self._value:
            return None

        if isinstance(self._value, str):
            try:
                self._value = datetime.fromisoformat(self._value)
            except Exception as e:
                raise DomainExceptionError(
                    f"Invalid datetime format for {self._cls_name}."
                ) from e

        if not isinstance(self._value, datetime):
            raise DomainExceptionError(
                f"Unsupported type for {self._cls_name}: "
                f"{type(self._value).__name__}"
            )

        # Normalize to UTC
        self._value = self._value.astimezone(tz=timezone.utc)
        self._validate_value_gt(incoming_time=self._value)
