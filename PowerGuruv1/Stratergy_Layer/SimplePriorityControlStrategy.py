from PriorityControlStratergy import PriorityControlStratergy
import sys

sys.path.append("C:/Users/sanka.liyanage/EMSDesign/PowerGuruv1/Facade_Layer/")
from IoTDeviceFacadeimpl import IoTDeviceFacadeimpl


class SimplePriorityControlStrategy(PriorityControlStratergy):
    def __init__(self) -> None:
        super().__init__()

    def execute(self, facade: IoTDeviceFacadeimpl) -> None:
        for device_id in facade._devices.keys():
            try:
                power = facade.get_power_consumption(device_id)
                if power > 100:
                    facade.turn_off(device_id)
                else:
                    facade.turn_on(device_id)
            except ValueError as e:
                print(e)
