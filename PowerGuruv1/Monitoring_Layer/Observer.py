from abc import ABC, abstractmethod


class Observer(ABC):

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def update(self, device_id: int, power_consumption: int) -> None:
        pass
