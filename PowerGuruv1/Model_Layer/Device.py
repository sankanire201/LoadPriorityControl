from abc import ABC, abstractmethod


class Device(ABC):

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def turn_on(self) -> None:
        pass

    @abstractmethod
    def turn_off(self) -> None:
        pass

    @abstractmethod
    def get_power_consumption(self) -> None:
        pass

    @abstractmethod
    def set_power_consumption(self, power: int) -> None:
        pass

    @abstractmethod
    def get_device_id(self) -> int:
        pass
