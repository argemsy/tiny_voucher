# Standard Libraries
from enum import Enum


class EnumChoice(Enum):
    @classmethod
    def choices(cls):
        return ((obj.value, obj.name) for obj in cls)


class EventBusTopicEnum(EnumChoice):
    CREATE_CAMPAIGN = "CREATE_CAMPAIGN"
    CREATE_VOUCHERS = "CREATE_VOUCHERS"
    UPDATE_CAMPAIGN = "UPDATE_CAMPAIGN"


class AuditLogObjectTypeEnum(EnumChoice):
    CAMPAIGN = "CAMPAIGN"
    VOUCHER = "VOUCHER"
    VOUCHER_REDEMPTION = "VOUCHER_REDEMPTION"


class AuditLogActionTypeEnum(EnumChoice):
    ADDITION = "ADDITION"
    CHANGE = "CHANGE"
    DELETION = "DELETION"


class AuditLogSourceTypeEnum(EnumChoice):
    ADMIN = "ADMIN"
    API = "API"
    COMMAND = "COMMAND"


class ResourceScopeEnum(EnumChoice):
    ADMIN = "Administrator"
    COLLABORATOR = "Collaborator"


class ErrorSchemaEnum(EnumChoice):
    VALIDATION_ERROR = "VALIDATION"
    INTEGRITY_ERROR = "INTEGRITY"
    INTERNAL_ERROR = "INTERNAL"


class DiscountTypeEnum(EnumChoice):
    PERCENTAGE = "PERCENTAGE"
    FIXED = "FIXED_VALUE"
