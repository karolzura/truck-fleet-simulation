# Fleet Logistics Simulator

## Overview
A modular Python-based simulation engine designed to track and manage a fleet of delivery trucks. This project is built with scalability in mind, using **Pydantic** for data validation and **Asyncio** for real-time telemetry updates.

## Tech Stack
- **Language:** Python 3.10+
- **Data Validation:** Pydantic
- **Asynchronous Engine:** Asyncio
- **Roadmap:** Integration with C++ for route optimization (TSP) and FastAPI for web access.

## Project Structure
- `trucks.py`: Core logic for individual truck behavior and movement.
- `fleetManager.py`: Management layer for coordinating multiple truck entities.
- `model.py`: Data schemas and validation rules.
- `main.py`: Entry point for the simulation loop.

## How to Run
1. Clone the repository.
2. Install dependencies: `pip install pydantic`
3. Run the simulation: `python main.py`
