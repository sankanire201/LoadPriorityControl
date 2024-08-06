from abc import ABC, abstractmethod


class CommunicationService(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def check_health(self) -> None:
        pass
