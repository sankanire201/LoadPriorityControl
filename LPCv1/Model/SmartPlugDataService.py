import sys
sys.path.append("/home/sanka/NIRE_EMS/volttron/LoadPriorityControl/LPCv1/")
from Model.GroupRepository import GroupRepository
from Model.IoTDeviceGroup import IoTDeviceGroup
import logging

logger = logging.getLogger(__name__)

class SmartPlugDataService:
    def __init__(self, repository:GroupRepository ) -> None:
        self._repository=repository
        self._control_commands={}
    
    def create_and_store_smart_plug_json(self, group: IoTDeviceGroup )->None:
        smart_plug_data = {}
        for key in group._devices:
            parts = key.split('/')
            # Extract parts
            first_part, second_part = parts[0], parts[1]
            device = group._devices[key]

            # Create nested dictionary structure
            smart_plug_data.setdefault('Monitor', {}).setdefault(first_part, {}).setdefault(second_part, {})[device._id] = {
                'power': device._power_consumption,
                'status': device._status,
                'priority': device._priority,
                'command' : device._last_command,
                'maxpower' : device._max_power_rating,
                'current' :device._current,
                'voltage' :device._voltage,
                'frequency' : device._frequency
            }
            smart_plug_data['Control']=self._control_commands
            
        logger.info(f"Loger Data >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> {smart_plug_data}")
        self._repository.update_Facade(smart_plug_data)
        
    def store_Control_Commands(self,command,agent)->None:
        self._control_commands[str(agent)]={'cmd':command}
        
        