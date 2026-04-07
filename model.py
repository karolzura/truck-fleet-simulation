from pydantic import BaseModel

class TruckData(BaseModel):
    id: str
    speed: float
    lat: float
    lng: float
    fuel: float
    fuel_lvl: str
