import sys
sys.path.append("C:/Users/sanka.liyanage/EMSDesign/LPCv1/")
from Controller.ControlStrategy import ControlStrategy
from Model.IoTFacade import IoTFacade

class EMSControl:
    
    def __init__(self,controlstrategy: ControlStrategy, devicegroup: IoTFacade) -> None:
        self._controlstratagey=controlstrategy
        self._devicegroup=devicegroup
        
    def execute_Strategy(self,message:any)->None:
        self._controlstratagey.execute(self._devicegroup,30)
        
    