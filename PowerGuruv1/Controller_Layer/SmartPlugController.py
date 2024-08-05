import sys

sys.path.append("C:/Users/sanka.liyanage/EMSDesign/PowerGuruv1/Facade_Layer/")
sys.path.append("C:/Users/sanka.liyanage/EMSDesign/PowerGuruv1/Stratergy_Layer/")
sys.path.append("C:/Users/sanka.liyanage/EMSDesign/PowerGuruv1/Model_Layer/")
from Device import Device
from PriorityControlStratergy import PriorityControlStratergy
from IoTDeviceFacade import IoTDeviceFacade


class SmartPlugController:
    def __init__(self, facade: IoTDeviceFacade) -> None:
        self._facade = facade
        self._strategy = None

    def add_smart_plug(self, device: Device) -> None:
        self._facade.add_device(device)

    def set_strategy(self, stratagy: PriorityControlStratergy) -> None:
        self._strategy = stratagy

    def execute_strategy(self) -> None:
        self._strategy.execute(self._facade)
