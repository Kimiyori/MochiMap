from abc import abstractmethod
from typing import Protocol, TypeVar

D = TypeVar("D", bound=object)
P = TypeVar("P", bound=object)


class ModelMapper(Protocol[D, P]):
    @staticmethod
    @abstractmethod
    def map_to_domain_entity(model: P) -> D: ...

    @staticmethod
    @abstractmethod
    def map_to_persistence_entity(model: D) -> P: ...
