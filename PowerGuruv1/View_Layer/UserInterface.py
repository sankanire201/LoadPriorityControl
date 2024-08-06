import sys
sys.path.append("C:/Users/sanka.liyanage/EMSDesign/PowerGuruv1/Model_Layer/")
from Device import Device

class UserInterface:
    
    def __init__(self) -> None:
        pass
    
    def display_status(devices:dict)->None:
        for device in devices:
            print(device, devices[device].get_power_consumption())