from Observable import Observable
from CommunicationService import CommunicationService
import sys
from Device import Device

sys.path.append("C:/Users/sanka.liyanage/EMSDesign/PowerGuruv1/Monitoring_Layer/")
from Observer import Observer


class SmartLight(Observable, CommunicationService, Device):
    def __init__(self) -> None:
        super().__init__()
        self._id = 1
        self._status = 1
        self._power_consumption = 2
        self._connected = True
        self._observer = []

    def register_Observer(self, observer: Observer) -> None:
        self._observer.append(observer)

    def remove_observer(self, observer: Observer) -> None:
        self._observer.remove(observer)

    def notify_observers(self) -> None:
        self._observer.update(self._id, self._power_consumption)

    def connect(self):
        print("connecting")
        self._connected = True
        return self._connected

    def check_health(self):
        print("Checking Health")
        self._status = 8

    def turn_on(self) -> None:
        print("Turn On")

    def turn_off(self) -> None:
        print("Turn offf")

    def get_power_consumption(self) -> None:
        return self._power_consumption

    def set_power_consumption(self, power: int) -> None:
        self._power_consumption = power

    def get_device_id(self) -> int:
        return self._id
