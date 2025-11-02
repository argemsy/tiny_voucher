# Third-party Libraries
import structlog
from django.db import connection, models, transaction
from django.db.utils import ProgrammingError

logger = structlog.getLogger(__name__)


class AuditModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True

    @classmethod
    def truncate(cls):
        """
        Truncates the table and resets the ID sequence to start from 1 (PostgreSQL only).
        Handles protected foreign key relationships by deleting related objects recursively.
        """
        log_tag = f"{cls.__name__}.truncate"

        with transaction.atomic():
            # Then delete the objects
            cls.objects.all().delete()

            if connection.vendor == "postgresql":
                table = cls._meta.db_table
                pk_column = cls._meta.pk.column
                sequence_name = f"{table}_{pk_column}_seq"

                try:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            f"ALTER SEQUENCE {sequence_name} RESTART WITH 1"
                        )
                except ProgrammingError as e:
                    logger.warning(
                        f"***{log_tag}*** Failed to reset the sequence: {e!r}"
                    )
            else:
                logger.error(
                    f"***{log_tag}*** Sequence reset not supported for the database engine '{connection.vendor}'"
                )


class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(blank=True, null=True, editable=False)
    deleted_by = models.IntegerField(db_index=True, blank=True, null=True)

    class Meta:
        abstract = True
