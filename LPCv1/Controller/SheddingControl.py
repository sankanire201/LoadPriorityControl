import sys
sys.path.append("C:/Users/sanka.liyanage/EMSDesign/LPCv1/")
from Model.IoTDeviceGroup import IoTDeviceGroup
from Controller.ControlStrategy import ControlStrategy
import logging
logger = logging.getLogger(__name__)

class SheddingControl(ControlStrategy):
    
    def __init__(self) -> None:
        super().__init__()
        
    def execute(self,group: IoTDeviceGroup, cmd: any) -> None:
        return super().execute()