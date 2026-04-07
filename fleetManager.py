from typing import List
from trucks import Truck
from model import TruckTelemetry

class FleetManager:
    def __init__(self):

        self.trucks: List[Truck] = []

    def add_starter_fleet(self, count: int = 10) -> None:
        for i in range(count):
            new_id = f"TRUCK-{i:02d}"  
            self.trucks.append(Truck(new_id, 60, 54.35, 18.64, 100))

    async def update_all(self) -> None:
        for truck in self.trucks:
            truck.move()
            truck.fuel_status()

    def get_fleet_telemetry(self) -> List[TruckTelemetry]:
        return [truck.get_telemetry() for truck in self.trucks]