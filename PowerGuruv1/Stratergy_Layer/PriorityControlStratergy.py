from abc import ABC, abstractmethod
import sys

sys.path.append("C:/Users/sanka.liyanage/EMSDesign/PowerGuruv1/Facade_Layer/")
from IoTDeviceFacadeimpl import IoTDeviceFacadeimpl


class PriorityControlStratergy(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def execute(self, facade: IoTDeviceFacadeimpl) -> None:
        pass
