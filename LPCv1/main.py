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

def Command(topic,cmd) -> dict:
    message={}
    message['topic']=topic
    message['Message']=cmd
    
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
    emscontroller = EMSControl()
    emscontroller.add_Controller(controlsimple)
    emscontroller.set_Group(group)
    emscontroller.add_Controller(controldirect)
    emscontroller.add_Controller(controlincrement)
    emscontroller.add_Controller(controlshed)
    
    """Assign smart Plugs to the Group Facade
    """    
    smart_plugs={}
    for i in plugsid:
        plug=SmartPlug(i,1)
        group.add_Device(plug)
        monitor.register_Observer(plug)
        smart_plugs[i]=plug
        
    """Updating Observers to update power consumption of each plug
    """
    
    monitor.set_EMS_Controller(emscontroller)
    
    monitor.process_Message(Message("devices/building540/NIRE_WeMo_cc_1/w1/all",200,1,2))
    monitor.process_Message(Message("devices/building540/NIRE_WeMo_cc_1/w2/all",20,1,2))
    monitor.process_Message(Message("devices/building540/NIRE_WeMo_cc_1/w3/all",500,1,1))
    monitor.process_Message(Message("devices/building540/NIRE_WeMo_cc_1/w4/all",400,1,5))
    monitor.process_Message(Command("control/building540/simple",30))
    monitor.process_Message(Command("control/building540/direct",command))   
    monitor.process_Message(Command("control/building540/shed",command)) 
    monitor.process_Message(Command("control/building540/increment",command)) 
    
    
    sorted_smart_plugs_pr = sorted(
    smart_plugs.values(),
    key=lambda plug: (plug._priority),reverse=True
    )
    
    sorted_smart_plugs_p = sorted(
    smart_plugs.values(),
    key=lambda plug: (plug._power_consumptiom),reverse=True
    )
# Output the sorted list
    for plug in sorted_smart_plugs_pr:
        print(plug._priority)
    
# Output the sorted list
    for plug in sorted_smart_plugs_p:
        print(plug._power_consumptiom)
        
    
    #emscontroller.execute_Strategy(1)
    
    #controlsimple.execute(group,30)
    #controlsimple.execute(group,command)    
    
if __name__ == "__main__":
    
    main()
    
    
    

