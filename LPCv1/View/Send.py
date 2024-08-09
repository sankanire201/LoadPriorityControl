
import sys
sys.path.append("C:/Users/sanka.liyanage/EMSDesign/LPCv1/Model/")
from View.Publish import Publish
from Model.IoTMessage import IoTMessage
class Send(Publish):
    def __init__(self,vip) -> None:
        super().__init__()
        self._vip=vip
        
    def publish(self, message: IoTMessage) -> bool:
        print("Sending",message)