
import sys
sys.path.append("C:/Users/sanka.liyanage/EMSDesign/LPCv1/")
from Model.IoTFacade import IoTFacade
from Model.IoTDevice import IoTDevice
from Model.SmartPlug import SmartPlug
import logging
logger = logging.getLogger(__name__)


class IoTDeviceGroup(IoTFacade):
    """_summary_
    This class extend the IoTFacade interface to implements the methods to manage and control group of IoT devices
    Args:
        IoTFacade (_type_): _description_
    """    
    def __init__(self) -> None:
        super().__init__()
        self._devices={}
        
    def turn_On(self, device_id: int) -> None:
        if bool(self._devices):
            print("turn_On")
            self._devices[device_id].turn_On()
        else:
            try:
                raise ValueError("the facade is empty: did you add devices to facade ?")
            except ValueError as e:
                logger.error(f"Error in IoTDevice group turnon method: {e}")
    
    def turn_Off(self, device_id: int) -> None:
        if bool(self._devices):
            print("turn_Off")
            self._devices[device_id].turn_Off()
        else:
            try:
                raise ValueError("the facade is empty: did you add devices to facade ?")
            except ValueError as e:
                logger.error(f"Error in IoTDevice group turnon method: {e}")
    
    def get_Power_Consumption(self, device_id: int) -> int:
        return self._devices[device_id].get_Power_Consumption()
    
    def set_Priority(self, device_id: int, priority: int) -> None:
        self._devices[device_id].set_Priority(priority)
        
    def get_Priority(self, device_id: int) -> int:
        return self._devices[device_id].set_Priority()
    
    def add_Device(self, device: IoTDevice) -> None:
        self._devices[device._id]=device
    
    def remove_Device(self, device: IoTDevice) -> None:
        try:
            if self._devices:
                del self._devices[device._id]
            else:
                try:
                    raise ValueError("Facade is Empty")
                except ValueError as e:
                    logger.error(f"Facade is Empty {e}")
        except Exception as e:
                logger.error(f"Error in the Facade: {e}")

    
    def get_Devices(self) -> dict:
        return self._devices
    
    def all_On(self) -> None:
        for device in self._devices:
            self.turn_On(device._id)
    
    def all_Off(self) -> None:
        for device in self._devices:
            self.turn_On(device._id)
    
# if __name__ == "__main__":
#         plug1 =SmartPlug(1,1)
#         plug2 =SmartPlug(2,1)
#         plug3 =SmartPlug(3,1)
        
#         control=SimpleControlStrategy()
#         plug1.set_Power_Consumption(100)
#         plug2.set_Power_Consumption(30)
#         plug3.set_Power_Consumption(200)
        
#         group = IoTDeviceGroup()
#         group.add_Device(plug1)
#         group.add_Device(plug2)
#         group.add_Device(plug3)
        
#         control.execute(group)