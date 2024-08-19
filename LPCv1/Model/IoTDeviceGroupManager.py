import sys
sys.path.append("/home/sanka/NIRE_EMS/volttron/LoadPriorityControl/LPCv1/")

from LoadPriorityControl.LPCv1.Model.IoTDeviceGroup import IoTDeviceGroup
from Model.IoTFacadeManager import IoTFacadeManager
import logging
from itertools import groupby
from Controller.DirectControl import DirectControl
from Controller.SheddingControl import SheddingControl
from Controller.IncrementalControl import IncrementalControl
from Controller.LoadPriorityControl import LoadPriorityControl
logger = logging.getLogger(__name__)


class IoTDeviceGroupManager(IoTFacadeManager):
    
    def __init__(self) -> None:
        super().__init__()
        self._groups=[]
        self._group_control_stratagey={}
        self._sorted_groups={}
        
    def group_By_Priority(self) -> IoTDeviceGroup:
        for group in self._groups:
            sorted_smart_plugs = sorted(group._devices.values(),key=lambda plug: plug._priority)
            for key, group in groupby(sorted_smart_plugs, key=lambda plug: plug._priority):
                temp= IoTDeviceGroup()
                for device in group:temp.add_Device(device)
                self._sorted_groups[key] = temp
        return self._sorted_groups
        
    def clear_Groups_Stratgies(self) -> None:
        self._group_control_stratagey={}
    
    def add_Group(self, group: IoTDeviceGroup) -> None:
        if group in self._groups:
            logger.error(f"The item is already exist in the list")
            raise KeyError('The Item is already in the list')
        else:
            self._groups.append(group)
    
    def remove_Group(self, group: IoTDeviceGroup) -> None:
        if not self._groups:
            logger.error(f"The list is empty")
            raise KeyError("The list is empty")
        else:
            self._groups.remove(group)
        
    def execute_Strategy(self)->None:
        
        if not self._group_control_stratagey:
            logger.warning(f"The group stratagies are empty")
            raise Warning("The group stratagies are empty")
        else:
            for group in self._group_control_stratagey.keys(): self._group_control_stratagey[group][0].execute(group,self._group_control_stratagey[group][1])
 
    
    def set_Group_Stratagy(self,group,cmd) -> None:
        if cmd[0]=='direct':
            self._group_control_stratagey[group]=(DirectControl(),cmd)
        elif cmd[0]=='increment':
            self._group_control_stratagey[group]=(IncrementalControl(),cmd)
        elif cmd[0]=='shed':
            self._group_control_stratagey[group]=(SheddingControl(),cmd)
        elif cmd[0]=='lpc':
            self._group_control_stratagey[group]=(LoadPriorityControl(),cmd)
        logger.info(f"Here is the group controllers >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>{self._group_control_stratagey}and the control input {cmd}")