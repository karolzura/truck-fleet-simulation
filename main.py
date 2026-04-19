from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime
from typing import List, Optional
import asyncio

from fleetManager import FleetManager
from model import TruckData, Order, FleetMetrics, Alert, DispatchRequest, DispatchResult

manager = FleetManager()


async def simulation_loop():
    while True:
        await manager.update_all()
        await asyncio.sleep(1)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(simulation_loop())
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


app = FastAPI(
    title="Fleet Operations API",
    description="Real-time fleet routing and dispatch system with deadline-aware optimization.",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Fleet ────────────────────────────────────────────────────────────

@app.get("/fleet", response_model=List[TruckData])
async def get_fleet():
    return manager.get_fleet_data()


@app.get("/fleet/{truck_id}", response_model=TruckData)
async def get_truck(truck_id: str):
    data = manager.get_truck(truck_id)
    if data is None:
        raise HTTPException(status_code=404, detail=f"Truck '{truck_id}' not found")
    return data


@app.post("/fleet", response_model=TruckData, status_code=201)
async def add_truck():
    return manager.add_truck()


@app.delete("/fleet/{truck_id}", status_code=204)
async def remove_truck(truck_id: str):
    if not manager.remove_truck(truck_id):
        raise HTTPException(status_code=404, detail=f"Truck '{truck_id}' not found")


# ── Orders ───────────────────────────────────────────────────────────

class OrderRequest(Order):
    id: Optional[str] = None
    status: Optional[str] = None
    assigned_to: Optional[str] = None
    delivered_at: Optional[datetime] = None


from pydantic import BaseModel

class CreateOrderRequest(BaseModel):
    city: str
    lat: float
    lng: float
    priority: int
    deadline: datetime


@app.post("/orders", response_model=Order, status_code=201)
async def create_order(req: CreateOrderRequest):
    return manager.add_order(
        city=req.city,
        lat=req.lat,
        lng=req.lng,
        priority=req.priority,
        deadline=req.deadline,
    )


@app.get("/orders", response_model=List[Order])
async def get_orders(status: Optional[str] = None):
    orders = manager.get_orders()
    if status:
        orders = [o for o in orders if o.status == status]
    return orders


@app.post("/dispatch", response_model=DispatchResult)
async def dispatch(req: DispatchRequest):
    result = manager.dispatch(req.truck_id, req.order_id)
    return DispatchResult(
        success=result["success"],
        truck_id=req.truck_id,
        order_id=req.order_id,
        reason=result["reason"],
    )

@app.get("/metrics", response_model=FleetMetrics)
async def get_metrics():
    return manager.get_metrics()


@app.get("/alerts", response_model=List[Alert])
async def get_alerts(limit: int = 50):
    return manager.get_alerts(limit)