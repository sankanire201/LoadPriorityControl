from abc import ABC, abstractmethod

class Observer(ABC):
    
    def __init__(self) -> None:
        super().__init__()
        
    @abstractmethod    
    def update(self,power_consumption :int) -> None:
        pass