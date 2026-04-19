from __future__ import annotations
 
from datetime import datetime
from typing import Optional
 
from pydantic import BaseModel
 
 
class TruckData(BaseModel):
    id: str
    speed: float
    lat: float
    lng: float
    fuel: float
    fuel_lvl: str
    state: str
    order_id: Optional[str] = None
    target: Optional[str] = None
 
 
class Order(BaseModel):
    id: str
    city: str
    lat: float
    lng: float
    priority: int
    deadline: datetime
    status: str = "PENDING"
    assigned_to: Optional[str] = None
    delivered_at: Optional[datetime] = None
 
 
class FleetMetrics(BaseModel):
    total_orders: int
    delivered_on_time: int
    delivered_late: int
    pending: int
    in_progress: int
    on_time_rate: float
    avg_fuel_per_delivery: float
 
 
class Alert(BaseModel):
    truck_id: Optional[str]
    order_id: Optional[str]
    level: str
    message: str
    timestamp: datetime
 
 
class DispatchRequest(BaseModel):
    truck_id: str
    order_id: str
 
 
class DispatchResult(BaseModel):
    success: bool
    truck_id: str
    order_id: str
    reason: str
