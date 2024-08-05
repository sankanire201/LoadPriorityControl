from IoTDeviceFacade import IoTDeviceFacade
import sys

sys.path.append("C:/Users/sanka.liyanage/EMSDesign/PowerGuruv1/Model_Layer/")
from Device import Device


class IoTDeviceFacadeimpl(IoTDeviceFacade):
    def __init__(self) -> None:
        super().__init__()
        self._devices = {}

    def turn_on(self, device_id: int) -> None:
        self._devices[device_id].turn_on()

    def turn_off(self, device_id: int) -> None:
        self._devices[device_id].turn_off()

    def get_power_consumption(self, device_id: int) -> None:
        return self._devices[device_id].get_power_consumption()

    def add_device(self, device: Device) -> None:
        self._devices[device.get_device_id()] = device

    def connect_device(self, device_id: int) -> None:
        return super().connect_device(device_id)

    def check_device_health(self, device_id: int) -> None:
        return super().check_device_health(device_id)

    def set_power_consumption(self, device_id: int, power: int) -> None:
        self._devices[device_id].set_power_consumption(power)
