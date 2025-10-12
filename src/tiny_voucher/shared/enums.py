# Standard Libraries
from enum import Enum


class EnumChoice(Enum):
    @classmethod
    def choices(cls):
        return ((obj.value, obj.name) for obj in cls)


class DiscountTypeEnum(EnumChoice):
    PERCENTAGE = "PERCENTAGE"
    FIXED = "FIXED_VALUE"
