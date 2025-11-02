# Standard Libraries
from abc import ABC
from typing import Generic, Optional, Type, TypeVar

_EntityT = TypeVar("_EntityT")
_ModelT = TypeVar("_ModelT")


class BaseRepository(ABC, Generic[_ModelT, _EntityT]):
    """Abstract base class for repositories.

    Provides a framework-agnostic contract for data persistence and retrieval
    between domain entities and infrastructure models.

    """

    entity_cls: Optional[Type[_EntityT]] = None
    model_cls: Optional[Type[_ModelT]] = None

    # ---------------------------
    # Validation helpers
    # ---------------------------
    def get_model_cls(self) -> Type[_ModelT]:
        """Return the registered model class or raise if missing."""
        if not self.model_cls:
            cls_name = self.__class__.__name__
            raise ValueError(f"Model for {cls_name} was not registered.")
        return self.model_cls

    def get_entity_cls(self) -> Type[_EntityT]:
        """Return the registered entity class or raise if missing."""
        if not self.entity_cls:
            cls_name = self.__class__.__name__
            raise ValueError(f"Entity for {cls_name} was not registered.")
        return self.entity_cls
