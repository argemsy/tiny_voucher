# Standard Libraries
import uuid
from typing import Optional, Union

# Own Libraries
from src.tiny_voucher.shared.exceptions import (
    DomainExceptionError,
    ValueObjectExceptionError,
)


class UUIDValueObject:
    """Value Object for validating and normalizing UUIDs.

    Ensures the value is a valid UUID (either string or uuid.UUID
    instance).

    It normalizes all values into uuid.UUID type and raises explicit
    domain exceptions if the input is invalid.
    """

    def __init__(self, value: Optional[Union[str, uuid.UUID]]):
        self._cls_name = self.__class__.__name__
        self._value = value
        self._check_value()

    @property
    def value(self) -> Optional[str]:
        """Returns the normalized UUID value."""
        return str(self._value) if self._value else None

    def _check_value(self) -> None:
        """Validates and normalizes the internal UUID value."""
        if self._value is None:
            raise ValueObjectExceptionError(
                f"Invalid value in {self._cls_name}. Value cannot be None."
            )

        # If already a UUID, just keep it
        if isinstance(self._value, uuid.UUID):
            return

        # If string, try to parse it
        if isinstance(self._value, str):
            try:
                self._value = uuid.UUID(self._value)
            except (ValueError, AttributeError) as e:
                raise DomainExceptionError(
                    f"Invalid UUID format for {self._cls_name}: '{self._value}'."
                ) from e
            return

        # Unsupported type
        raise DomainExceptionError(
            f"Unsupported type for {self._cls_name}: {type(self._value).__name__}"
        )

    def __str__(self) -> str:
        """Returns string representation of the UUID."""
        return str(self._value)

    def __repr__(self) -> str:
        return f"<{self._cls_name}(value='{self._value}')>"

    def __eq__(self, other: object) -> bool:
        """Equality comparison based on UUID value."""
        if not isinstance(other, UUIDValueObject):
            return False
        return self.value == other.value

    def __hash__(self):
        """Allows usage as dictionary keys or set elements."""
        return hash(self._value)
