from abc import ABC, abstractmethod
import sys
sys.path.append("C:/Users/sanka.liyanage/EMSDesign/LPCv1/")
from Model.IoTDeviceGroup import IoTDeviceGroup

class ControlStrategy(ABC):
    
    def __init__(self) -> None:
        super().__init__()
        self._controlType=None
    
    @abstractmethod
    def execute(self,group:IoTDeviceGroup,cmd:any)->None:
        pass