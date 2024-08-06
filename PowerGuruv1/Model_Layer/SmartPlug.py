from Observable import Observable
from CommunicationService import CommunicationService
from Device import Device
import sys

sys.path.append("C:/Users/sanka.liyanage/EMSDesign/PowerGuruv1/Monitoring_Layer/")
sys.path.append("C:/Users/sanka.liyanage/EMSDesign/PowerGuruv1/Facade_Layer/")
sys.path.append("C:/Users/sanka.liyanage/EMSDesign/PowerGuruv1/Stratergy_Layer/")
sys.path.append("C:/Users/sanka.liyanage/EMSDesign/PowerGuruv1/Controller_Layer/")
sys.path.append("C:/Users/sanka.liyanage/EMSDesign/PowerGuruv1/View_Layer/")

from IoTDeviceFacadeimpl import IoTDeviceFacadeimpl
from Observer import Observer
from PowerConsumptionMonitor import PowerConsumptionMonitor
from SimplePriorityControlStrategy import SimplePriorityControlStrategy
from SmartPlugController import SmartPlugController
from UserInterface import UserInterface

class SmartPlug(Observable, CommunicationService, Device):

    def __init__(self, id: int,priority:int) -> None:
        super().__init__()
        self._id = id
        self._status = 2
        self._power_consumption = 0
        self._connected = False
        self._observers = []
        self._flagged=False
        self._last_command= None
        self._priority = priority

    def turn_on(self) -> None:
        if self._connected:
            self._last_command=1
            self._flagged=False
            print("turning_On Plug", self._id)
        else: 
            self._flagged=True
            

    def turn_off(self) -> None:
        if self._connected:
            self._last_command=0
            self._flagged=False
            print("Turning Off Plug", self._id)
        else:
            self._flagged=True

    def get_power_consumption(self) -> None:
        return self._power_consumption

    def set_power_consumption(self, power: int) -> None:
        self._power_consumption = power
        self.notify_observers()
        
    def set_priority(self,priority:int)->None:
        self._priority=priority
        
    def register_Observer(self, observer: Observer) -> None:
        self._observers.append(observer)

    def remove_observer(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify_observers(self) -> None:
        for observer in self._observers:
            observer.update(self._id, self._power_consumption)

    def connect(self) -> None:
        print("connecting")s
        self._connected = True

    def check_health(self) -> None:
        print("checking the status")

    def get_device_id(self) -> int:
        return self._id


if __name__ == "__main__":

    plug1 = SmartPlug(1)
    plug2 = SmartPlug(2)
    plug3 = SmartPlug(3)
    plug4 = SmartPlug(4)
    

    facade = IoTDeviceFacadeimpl()
    facade.add_device(plug1)
    facade.add_device(plug2)
    facade.add_device(plug3)
    facade.add_device(plug4)
    
    monitor = PowerConsumptionMonitor()
    plug1.register_Observer(monitor)
    plug2.register_Observer(monitor)
    plug3.register_Observer(monitor)
    plug4.register_Observer(monitor)
    
    
    plug1.set_power_consumption(100)
    plug2.set_power_consumption(300)
    plug3.set_power_consumption(70)
    plug4.set_power_consumption(20)
    
    print(facade.get_power_consumption(1), facade.get_power_consumption(2))
    print(facade.set_power_consumption(1, 500), facade.set_power_consumption(2, 30))

    strat = SimplePriorityControlStrategy()
    strat.execute(facade)


    controller = SmartPlugController(facade)
    controller.add_smart_plug(plug3)
    controller.add_smart_plug(plug4)
    controller.set_strategy(strat)
    controller.execute_strategy()
    
    Ui=UserInterface()
    UserInterface.display_status(facade._devices)
