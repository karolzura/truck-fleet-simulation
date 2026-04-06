import random 
import time 
import json
import asyncio
status = ["moving", "idle", "alert"]
lat = 54.3519
lng = 18.6463

class Truck:
    def __init__(self, truck_id, speed, x, y,fuel):
        self.truck_id = truck_id
        self.speed = speed
        self.x = x
        self.y = y
        self.fuel = fuel
        self.fuel_lvl = "OK"
    
    def move(self):
        self.x += random.uniform(-0.0001,0.0001)
        self.y += random.uniform(-0.0001,0.0001)
        self.fuel -= random.uniform(0.1,0.6)
        if self.fuel <= 0:
            self.speed = 0
            self.x += 0
            self.y += 0
    
    def fuel_status(self):
        if self.fuel <= 10:
            self.fuel_lvl = "LOW"
        elif self.fuel <= 0:
            self.fuel_lvl = "EMPTY"
    #returning truck info in json
    def to_dict(self):
        return {
            "id": self.truck_id,
            "speed": self.speed,
            "location": {"lat": round(self.x, 6), "lng": round(self.y, 6)},
            "fuel": round(self.fuel, 2),
            "fuel_lvl": self.fuel_lvl
        }


async def main():
    
    truck = Truck("Truck01",60,54.35,18.64,100)

    while True: 
        truck.move()
        truck.fuel_status()
        data = truck.to_dict()
        print(json.dumps(data, indent=2))
        await asyncio.sleep(1)
if __name__ == "__main__":
    asyncio.run(main())