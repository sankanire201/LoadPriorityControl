import sys
sys.path.append("C:/Users/sanka.liyanage/EMSDesign/LPCv1/")
from Model.Observer import Observer
from Model.IoTDevice import IoTDevice
from Model.IoTMessage import IoTMessage
from View.Send import Send
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class SmartPlug(Observer,IoTDevice):
    """_summary_
    The smart plug describes the methods to control and monitor a smart Plug
    Args:
        Observer ( Interface): observer for updating IoTdevice statusS
        IoTDevice ( Interface): Interface to use to derive the SmartPlug class
    """    
    def __init__(self,id :str,vip) -> None:
        """_summary_

        Args:
            id (int): device Id
            vip (obj): volttron vip connection for communication in the volttron message bus
        """        
        super().__init__()
        self._id=id
        self._status=0
        self._power_consumptiom=0
        self._connected=0
        self._flagged=False
        self._last_command=0
        self._priority=0
        self._vip=vip
        self._send=Send(vip)
        self._message= IoTMessage(device_id=id,message_type=None,payload=['command',None],timestamp=datetime.now())
        self._observerid=id
        
    def turn_On(self) -> None:
        self._message.message_type='command'
        self._message.payload={'cmd',1}
        self.publish()
        self._last_command=self._message
        
    
    def turn_Off(self) -> None:
        self._message.message_type='command'
        self._message.payload={'cmd',0}
        self.publish()
        self._last_command=self._message
    
    def get_Power_Consumption(self) -> int:
        return self._power_consumptiom
    
    def set_Power_Consumption(self, power: int) -> None:
        self._power_consumptiom = power
    
    def get_Device_Id(self) -> int:
        return self._id
    
    def set_Priority(self, priority: int) -> None:
        self._priority=priority
    
    def get_Priority(self) -> int:
        return self._priority
    
    def update(self, power_consumption: int, status: int, priority: int) -> None:
        """_summary_
        this method is executed by the observer when ever the power consumption is updated
        Args:
            power_consumption (int): instatntanious power consumption of the smart plug
        """        
        self.set_Power_Consumption(power_consumption)
        self._priority=priority
        self._status=status
        
    def _check_Health(self)-> None:
        pass
    
    def isFlaged(self)->None:
        return self._flagged == True
    
    def publish(self) -> bool:
        """_summary_
        this method publish the message to the volttron message bus
        Returns:
            bool: state of sending data
        """        
        self._send.publish(self._message)
        return bool
    
# if __name__ == "__main__":
    
#     plug = SmartPlug(1,1)
#     plug.turn_On()
#     plug.turn_Off()
#     print(plug.isFlaged())