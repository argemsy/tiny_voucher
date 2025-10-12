# Third-party Libraries
from django.db import models


class AuditModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(blank=True, null=True, editable=False)
    deleted_by = models.IntegerField(db_index=True, blank=True, null=True)

    class Meta:
        abstract = True
