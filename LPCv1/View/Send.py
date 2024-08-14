
import sys
sys.path.append("/home/sanka/NIRE_EMS/volttron/LoadPriorityControl/LPCv1/")
from View.Publish import Publish
from Model.IoTMessage import IoTMessage
class Send(Publish):
    def __init__(self,vip) -> None:
        super().__init__()
        self._vip=vip
        
    def publish(self, message: IoTMessage) -> bool:
        print("Sending",message)
        result=self._vip.rpc.call('platform.driver','set_point',message.device_id,'status',message.payload['cmd'],external_platform=message.device_id.split('/')[-2])
        