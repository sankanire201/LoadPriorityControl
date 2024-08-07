from Publish import Publish
from IoTMessage import IoTMessage
class Send(Publish):
    def __init__(self,vip) -> None:
        super().__init__()
        self._vip=vip
        
    def publish(self, message: IoTMessage) -> bool:
        print("Sending",message)