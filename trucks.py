import random 
from model import TruckData

class Truck:
    def __init__(self, truck_id, speed, x, y,fuel):
        self.truck_id = truck_id
        self.speed = speed
        self.x = x
        self.y = y
        self.fuel = fuel
        self.fuel_lvl = "OK"
    
    def move(self):
        if self.fuel <= 0:
            self.speed = 0
            return
        self.x += random.uniform(-0.0001, 0.0001)
        self.y += random.uniform(-0.0001, 0.0001)
        self.fuel -= random.uniform(0.1, 0.6)
    
    def fuel_status(self):
        if self.fuel <= 0:
            self.fuel_lvl = "EMPTY"
            self.fuel = 0  
        elif self.fuel <= 10:
            self.fuel_lvl = "LOW"
        else:
            self.fuel_lvl = "OK"

    def get_data(self) -> TruckData:
        return TruckData(
            id=self.truck_id,
            speed=self.speed,
            lat=round(self.x, 6),
            lng=round(self.y, 6),
            fuel=round(self.fuel, 2),
            fuel_lvl=self.fuel_lvl
        )
