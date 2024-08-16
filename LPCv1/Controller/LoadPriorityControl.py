import sys
sys.path.append("/home/sanka/NIRE_EMS/volttron/LoadPriorityControl/LPCv1/")
from Model.IoTDeviceGroup import IoTDeviceGroup
from Controller.ControlStrategy import ControlStrategy
import logging
logger = logging.getLogger(__name__)

class LoadPriorityControl(ControlStrategy):
    def __init__(self) -> None:
        super().__init__()
        self._controlType='lpc'
        
    def execute(self, group: IoTDeviceGroup, cmd: any) -> None:
        logger.info(f'Running Load Priority controller on the group {id(group)} with the power consumption of the group {group.get_Facade_Consumption()}')
        for device_id in group._devices: logger.info(f"the device id {device_id} has the priority: {group._devices[device_id]._priority}")
        