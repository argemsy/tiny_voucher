# Standard Libraries
from datetime import datetime
from typing import Optional

# Own Libraries
from src.tiny_voucher.shared.enums import (
    AuditLogActionTypeEnum,
    AuditLogObjectTypeEnum,
    AuditLogSourceTypeEnum,
)


class EntityAuditLog:
    """
    Domain Entity representing an Audit Log record.

    Represents an audit log entry within the domain layer, independent
    from Django or database concerns.
    """

    def __init__(
        self,
        object_id: str,
        object_type: AuditLogObjectTypeEnum,
        object_repr: str,
        action_type: AuditLogActionTypeEnum,
        source: AuditLogSourceTypeEnum,
        created_by: int,
        created_at: datetime,
        description: Optional[str] = None,
        metadata: Optional[dict] = None,
        id: Optional[int] = None,
    ):
        self.id = id
        self.object_id = object_id
        self.object_type = object_type
        self.object_repr = object_repr
        self.action_type = action_type
        self.source = source
        self.created_by = created_by
        self.created_at = created_at
        self.description = description or ""
        self.metadata = metadata or self._default_metadata()

    # ---------------------------
    # Factory method
    # ---------------------------
    @classmethod
    def from_model(cls, instance):
        """Creates an entity from a Django model instance."""
        return cls(
            id=instance.id,
            object_id=instance.object_id,
            object_type=AuditLogObjectTypeEnum[instance.object_type],
            object_repr=instance.object_repr,
            action_type=AuditLogActionTypeEnum[instance.action_type],
            source=AuditLogSourceTypeEnum[instance.source],
            created_by=instance.created_by,
            created_at=instance.created_at,
            description=instance.description,
            metadata=instance.metadata,
        )

    # ---------------------------
    # Internal helpers
    # ---------------------------
    @staticmethod
    def _default_metadata() -> dict:
        """Default metadata structure."""
        return {
            "version": 1,
            "update_fields": [],
            "message": "",
        }

    # ---------------------------
    # Utility
    # ---------------------------
    def to_dict(self) -> dict:
        """Converts entity to a serializable dictionary."""
        return {
            "id": self.id,
            "object_id": self.object_id,
            "object_type": self.object_type.value,
            "object_repr": self.object_repr,
            "action_type": self.action_type.value,
            "source": self.source.value,
            "description": self.description,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata,
        }

    def __repr__(self) -> str:
        return (
            f"<EntityAuditLog "
            f"{self.object_type.value}[{self.object_id}] "
            f"{self.action_type.value} by {self.created_by}>"
        )
