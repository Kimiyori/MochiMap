from abc import abstractmethod
from typing import TypeVar

RepositoryT = TypeVar("RepositoryT")


class BaseUseCase[RepositoryT]:
    def __init__(self, uow: RepositoryT) -> None:
        self.uow = uow

    @abstractmethod
    def invoke(self): ...
