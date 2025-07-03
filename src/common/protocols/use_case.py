from abc import abstractmethod


class BaseUseCase:
    @abstractmethod
    def invoke(self): ...
