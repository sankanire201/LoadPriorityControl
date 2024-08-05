from Observer import Observer


class PowerConsumptionMonitor(Observer):

    def __init__(self) -> None:
        super().__init__()
        self._threshold = 10

    def update(self, device_id: int, power_consumption: int) -> None:
        print(
            "Updating the Consumption for smart plug:",
            device_id,
            "Power consumption: ",
            power_consumption,
        )
