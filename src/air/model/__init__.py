"""Backend-agnostic Pydantic models with async persistence methods."""

from air.model.backend import (
    AirModelBackend as AirModelBackend,
    AirModelTransactionBackend as AirModelTransactionBackend,
    clear_model_backend as clear_model_backend,
    get_model_backend as get_model_backend,
    set_model_backend as set_model_backend,
)
from air.model.main import (
    AirModel as AirModel,
    MultipleObjectsReturned as MultipleObjectsReturned,
    Predicate as Predicate,
    Query as Query,
    registered_models as registered_models,
)

__all__ = [
    "AirModel",
    "AirModelBackend",
    "AirModelTransactionBackend",
    "MultipleObjectsReturned",
    "Predicate",
    "Query",
    "clear_model_backend",
    "get_model_backend",
    "registered_models",
    "set_model_backend",
]
