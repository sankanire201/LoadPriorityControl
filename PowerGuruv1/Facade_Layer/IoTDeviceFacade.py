from abc import ABC, abstractmethod


class IoTDeviceFacade(ABC):

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def turn_on(self, device_id: int) -> None:
        pass

    @abstractmethod
    def turn_off(self, device_id: int) -> None:
        pass

    @abstractmethod
    def get_power_consumption(self, device_id: int) -> None:
        pass

    @abstractmethod
    def add_device(self, device) -> None:
        pass

    @abstractmethod
    def set_power_consumption(self, device_id: int, power: int):
        pass

    @abstractmethod
    def connect_device(self, device_id: int) -> None:
        pass

    @abstractmethod
    def check_device_health(self, device_id: int) -> None:
        pass
