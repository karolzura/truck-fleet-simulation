from trucks import Truck
from fleetManager import FleetManager
from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio

manager = FleetManager()

async def run_simulation():
    manager.add_starter_fleet(5)
    while True:
        await manager.update_all()
        await asyncio.sleep(1)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(run_simulation())
    yield
    task.cancel()

app = FastAPI(lifespan=lifespan)

@app.get("/fleet")
async def get_fleet():
    return manager.get_fleet_data()
