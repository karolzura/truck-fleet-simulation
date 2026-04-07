from trucks import Truck
from fleetManager import FleetManager

async def main():
    manager = FleetManager()
    manager.add_starter_fleet(5)

    while True:
        await manager.update_all()
        telemetry = manager.get_fleet_data()
        
        print(f"Tracking {len(telemetry)} trucks...") 
        await asyncio.sleep(1)

if __name__ == "__main__":
    import asyncio
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Simulation stopped by user.")