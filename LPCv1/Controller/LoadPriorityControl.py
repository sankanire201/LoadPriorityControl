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
        # self.priority_groups = {}
        # for device in devices:
        #     if device.priority not in self.priority_groups:
        #         self.priority_groups[device.priority] = []
        #     self.priority_groups[device.priority].append(device)

        # for priority in self.priority_groups:
        #     # Sort devices within the same priority by their power consumption (ascending)
        #     self.priority_groups[priority].sort(key=lambda x: x.get_power_consumption())

        
    def execute(self, group: IoTDeviceGroup, cmd: any) -> None:
        logger.info(f'Running Load Priority controller on the group {id(group)} with the power consumption of the group {group.get_Facade_Consumption()}')
        for device_id in group._devices: logger.info(f"the device id {device_id} has the priority: {group._devices[device_id]._priority}")
        total_consumption = sum(group.get_Facade_Consumption().values())
        logger.info(f">>>>>>>>>>>>>>>>>>>>>>>>>>>> total consumption {total_consumption}, { self._group_by_Priorities(group)} . >>>>>>>>>>>>>>>>>>>>>>> {cmd}")
        decoded_cmd=cmd[1]
        if total_consumption > decoded_cmd:
             print("Threshold exceeded. Turning off devices...")
             priority_groups=self._group_by_Priorities(group,False)
        #     for priority in sorted(self.priority_groups.keys(), reverse=True):
        #         stack = self.priority_groups[priority]
        #         while total_consumption > group and stack:
        #             device = stack.pop(0)
        #             if device.status == 'on':
        #                 group.turn_off(device._id)
        #                 total_consumption -= device.get_power_consumption()

        elif total_consumption < decoded_cmd:
             print("Below threshold. Turning on devices...")
             priority_groups=self._group_by_Priorities(group,True)
             for priority in priority_groups.keys():
        #         stack = self.priority_groups[priority]
                 for device in priority_groups[priority]:
                     total_consumption += device._max_power_rating
                     if total_consumption < decoded_cmd and device._last_command==0:
                         #device.turn_On()
                         device._last_command=1
                         sleep(1)
                         logger.info(f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Turning on device {device._id} with priority {priority}, and total  consumption {total_consumption}")
                     else:
                         break
