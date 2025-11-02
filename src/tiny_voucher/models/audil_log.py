# Standard Libraries
from typing import Any

# Third-party Libraries
from django.db import models
from pydantic import BaseModel, Field

# Own Libraries
from src.tiny_voucher.shared.enums import (
    AuditLogActionTypeEnum,
    AuditLogObjectTypeEnum,
    AuditLogSourceTypeEnum,
)


class AuditLogUpdateField(BaseModel):
    field: str
    changes: dict[str, Any] = Field(default_factory=dict)


class AuditLogMetadata(BaseModel):
    version: int = Field(default=1)
    update_fields: list[AuditLogUpdateField] = Field(default_factory=list)
    message: str = Field(default="")


def metadata_default():
    return AuditLogMetadata().dict()


class AuditLogModel(models.Model):
    object_id = models.CharField(
        max_length=255,
        db_index=True,
    )
    object_type = models.CharField(
        max_length=50,
        db_index=True,
        choices=AuditLogObjectTypeEnum.choices(),
    )
    object_repr = models.CharField(max_length=255)
    action_type = models.CharField(
        max_length=50,
        db_index=True,
        choices=AuditLogActionTypeEnum.choices(),
    )
    source = models.CharField(
        max_length=50,
        db_index=True,
        choices=AuditLogSourceTypeEnum.choices(),
        default=AuditLogSourceTypeEnum.API.value,
    )
    description = models.TextField(blank=True, null=True)
    created_by = models.IntegerField(
        default=0,
        db_index=True,
        help_text="User with id 0 [Sys]",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=metadata_default)

    class Meta:
        db_table = "audit_logs"
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=[
                    "object_type",
                    "object_id",
                ],
                name="audit_obj_idx",
            ),
        ]

    def __str__(self):
        return f"{self.object_type}[{self.object_id}] {self.action_type}"
