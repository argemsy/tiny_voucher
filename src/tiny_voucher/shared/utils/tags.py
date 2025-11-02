# Standard Libraries
from typing import Optional

# Third-party Libraries
from pydantic import BaseModel

# Own Libraries
from src.tiny_voucher.shared.enums import ResourceScopeEnum


class ExternalDocs(BaseModel):
    description: Optional[str] = None
    url: str


class MetadataTag(BaseModel):
    name: str
    version: int
    scope: ResourceScopeEnum
    description: Optional[str] = None
    external_docs: Optional[ExternalDocs] = None

    class Config:
        use_enum_values = True
        allow_population_by_field_name = True
        fields = {
            "external_docs": {
                "alias": "externalDocs",
            },
        }
