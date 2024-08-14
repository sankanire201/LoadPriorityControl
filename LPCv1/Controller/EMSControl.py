import sys
sys.path.append("/home/sanka/NIRE_EMS/volttron/LoadPriorityControl/LPCv1/")
from Controller.ControlStrategy import ControlStrategy
from Model.IoTFacade import IoTFacade
import logging
logger = logging.getLogger(__name__)
class EMSControl:
    
    def __init__(self) -> None:
        self._controlstratagey={}
        self._devicegroup=None
        
    def execute_Strategy(self,message:any)->None:
        self._controlstratagey[message['controlType']][0].execute(self._devicegroup,message['cmd'])
        
    def add_Controller(self,controlstrategy:ControlStrategy) -> None:

            if controlstrategy._controlType  in self._controlstratagey:
                self._controlstratagey[controlstrategy._controlType].append(controlstrategy)
            else:
                self._controlstratagey[controlstrategy._controlType]=[]
                self._controlstratagey[controlstrategy._controlType].append(controlstrategy)

    def remove_Controller(self,controlstrategy:ControlStrategy)->None:
        if  self._controlstratagey:
            try:
                self._controlstratagey[controlstrategy._controlType].remove(controlstrategy)
            except Exception as e:
                logger.error(f"error in remove controller {e}")
        else:
            pass
        
    def set_Group(self,Group: IoTFacade) -> None:
        self._devicegroup=Group
    
            
    def remove_Group(self,Group: IoTFacade)->None:
        pass