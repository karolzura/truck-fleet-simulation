# Fleet Logistics Simulator

A full-stack fleet management dashboard simulating a delivery truck network across Poland. Orders are dispatched to trucks using a C++ routing engine with deadline-aware scoring and KD-tree spatial indexing, exposed via a FastAPI backend and visualized in a React frontend.

## Tech Stack

**Backend**
- Python 3.12, FastAPI, Asyncio
- C++ routing engine compiled as a Python extension via pybind11
- KD-tree spatial indexing for nearest-neighbor order lookup
- Pydantic for data validation

**Frontend**
- React 19 + Vite
- react-leaflet (interactive map of Poland)
- Polling every 2s

## Features

- Live map showing truck positions and active order pins
- Truck state machine: `IDLE → DRIVING → CRAWLING → REFUELING → STOPPED`
- Deadline-aware order scoring (priority × urgency − travel cost)
- Manual dispatch: assign any truck to any pending order
- Fleet metrics: on-time rate, avg fuel per delivery, order breakdown
- Alert feed: CRITICAL (unassigned order deadline < 60s), WARNING (late delivery)
- Add / remove trucks at runtime

## Project Structure

```
palantir-intern-project/
├── backend/
│   ├── core/
│   │   ├── include/        # C++ headers (Destination, KDTree, RouteEngine)
│   │   ├── src/            # C++ implementation
│   │   └── bindings.cpp    # pybind11 bindings
│   ├── main.py             # FastAPI app + simulation loop
│   ├── fleetManager.py     # Fleet orchestration
│   ├── trucks.py           # Truck state machine
│   ├── model.py            # Pydantic schemas
│   └── Dockerfile
├── frontend/
│   └── src/
│       ├── App.jsx          # Root: state, polling, layout
│       ├── api.js           # Fetch wrappers
│       ├── constants.js     # Cities, colors
│       └── components/      # FleetMap, FleetSidebar, MetricsBar,
│                            # OrderForm, DispatchPanel, AlertsFeed
│   └── Dockerfile
├── docker-compose.yml
└── setup.py                 # pybind11 build config
```

## Running with Docker (recommended)

```bash
docker compose up --build
```

- Dashboard: `http://localhost:5173`
- API docs: `http://localhost:8000/docs`

## Running locally

### 1. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Python dependencies

```bash
pip install fastapi "uvicorn[standard]" pydantic pybind11 setuptools
```

### 3. Build the C++ routing engine

```bash
cd backend
python3 ../setup.py build_ext --inplace
```

Repeat this step after any changes to `backend/core/`.

### 4. Start the backend

```bash
cd backend
../venv/bin/uvicorn main:app --reload
```

API available at `http://localhost:8000`. Docs at `http://localhost:8000/docs`.

### 5. Start the frontend

```bash
cd frontend
npm install
npm run dev
```

Dashboard available at `http://localhost:5173`.

