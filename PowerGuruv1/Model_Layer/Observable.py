from abc import ABC, abstractmethod


class Observable(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def register_Observer(self, observer) -> None:
        pass

    @abstractmethod
    def remove_observer(self, observer) -> None:
        pass

    @abstractmethod
    def notify_observers(self) -> None:
        pass
