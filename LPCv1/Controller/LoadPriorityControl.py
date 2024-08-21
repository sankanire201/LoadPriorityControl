import sys
sys.path.append("/home/sanka/NIRE_EMS/volttron/LoadPriorityControl/LPCv1/")
from Model.IoTDeviceGroup import IoTDeviceGroup
from Controller.ControlStrategy import ControlStrategy
import logging
from itertools import groupby
logger = logging.getLogger(__name__)
from time import sleep
class LoadPriorityControl(ControlStrategy):
    def __init__(self) -> None:
        super().__init__()
        self._controlType='lpc'
        self.priority_groups = {}
                
    def _group_by_Priorities(self, group,_reverse=False):
        sorted_groups={}
        sorted_smart_plugs = sorted(group._devices.values(),key=lambda plug: plug._priority,reverse=_reverse)
        for key, sortedgroup in groupby(sorted_smart_plugs, key=lambda plug: plug._priority):
                sorted_groups[key] = list(sortedgroup)
        return  sorted_groups
        
    def execute(self, group: IoTDeviceGroup, cmd: any) -> None:
        total_consumption = sum(group.get_Facade_Consumption().values())
        logger.info(f">>>>>>>>>>>>>>>>>>>>>>>>>>>> total consumption {total_consumption}, { self._group_by_Priorities(group)} . >>>>>>>>>>>>>>>>>>>>>>> {cmd}")
        decoded_cmd=cmd[1]
        ## Shedding control section 
        if total_consumption > decoded_cmd:
             logger.info("Threshold exceeded. Turning off devices...")
             priority_groups=self._group_by_Priorities(group,False)
             for priority in priority_groups.keys():
                for device in priority_groups[priority] :
                    if total_consumption > decoded_cmd and device._power_consumption>0:
                        device.turn_Off()
                        device._last_command=0
                        sleep(1)
                        logger.info(f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Turning off device {device._id} with priority {priority}, and total  consumption {total_consumption}")
                        total_consumption -= device._power_consumption       
                    else:
                        break
                                  
        ## Incremental control section 
        elif total_consumption < decoded_cmd-100:
             logger.info("Below threshold. Turning on devices ........ >>>>>>>>>>>>>>>>>>>>>>>>")
             priority_groups=self._group_by_Priorities(group,True)
             max_rating=sum(group. get_Facade_Max_rating().values())
             for priority in priority_groups.keys():
                 for device in priority_groups[priority]:
                     total_consumption += device._max_power_rating
                     if total_consumption < decoded_cmd and device._last_command==0:
                         device.turn_On()
                         device._last_command=1
                         sleep(1)
                         logger.info(f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Turning on device {device._id} with priority {priority}, and total  consumption {total_consumption}")
                     else:
                         break
