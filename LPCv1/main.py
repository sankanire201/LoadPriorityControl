import sys
sys.path.append("C:/Users/sanka.liyanage/EMSDesign/LPCv1/")

from Model.SmartPlug import SmartPlug
from Model.IoTDeviceGroup import IoTDeviceGroup
from Controller.SimpleControlStrategy import SimpleControlStrategy
from Controller.DeviceMonitor import DeviceMonitor
from Controller.DirectControl import DirectControl
from Controller.SheddingControl import SheddingControl
from Controller.IncrementalControl import IncrementalControl
from Controller.EMSControl import EMSControl

def Message(topic,power,status,priority) -> dict:
    message={}
    message['topic']=topic
    message['Message']={'power':power,'status':status,'priority':priority}
    
    return message

def main():
    
    """
    Defining variables
    """
    plugsid = ['w1','w2','w3', 'w4']
    command ={'w1':1,'w2':0,'w3':1,'w4':0}
    group = IoTDeviceGroup() # Group Facade
    monitor = DeviceMonitor() # Monitor for smart plug update
    controlsimple =  SimpleControlStrategy()
    controldirect = DirectControl()
    controlshed = SheddingControl()
    controlincrement = IncrementalControl()
    emscontroller = EMSControl(controlsimple,group)
    
    """Assign smart Plugs to the Group Facade
    """    
    for i in plugsid:
        plug=SmartPlug(i,1)
        group.add_Device(plug)
        monitor.register_Observer(plug)
        
    """Updating Observers to update power consumption of each plug
    """
    
    monitor.set_EMS_Controller(emscontroller)
    
    monitor.process_Message(Message("devices/building540/NIRE_WeMo_cc_1/w1/all",200,1,1))
    monitor.process_Message(Message("devices/building540/NIRE_WeMo_cc_1/w2/all",20,1,2))
    monitor.process_Message(Message("devices/building540/NIRE_WeMo_cc_1/w3/all",500,1,1))
    monitor.process_Message(Message("devices/building540/NIRE_WeMo_cc_1/w4/all",400,1,3))
    monitor.process_Message(Message("control/building540/NIRE_WeMo_cc_1/w1/all",200,1,1))
    
    #emscontroller.execute_Strategy(1)
    
    #controlsimple.execute(group,30)
    #controlsimple.execute(group,command)    
    
if __name__ == "__main__":
    
    main()
    
    
    

