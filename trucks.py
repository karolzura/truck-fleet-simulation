import math
from datetime import datetime, timezone
from model import TruckData

try:
    from simulation_engine import RouteEngine
    _ENGINE_AVAILABLE = True
except ImportError:
    _ENGINE_AVAILABLE = False

STATE_DRIVING   = "DRIVING"
STATE_REFUELING = "REFUELING"
STATE_CRAWLING  = "CRAWLING"
STATE_STOPPED   = "STOPPED"
STATE_IDLE      = "IDLE"

REFUEL_TICKS  = 5
FUEL_CAPACITY = 100.0
STEP_SIZE     = 0.01
FUEL_BURN     = 0.3

START_LAT = 52.23
START_LNG = 21.01


class Truck:
    def __init__(self, truck_id: str, speed: float, fuel: float):
        self.truck_id    = truck_id
        self.speed       = speed
        self.base_speed  = speed
        self.x           = START_LAT
        self.y           = START_LNG
        self.fuel        = fuel
        self.fuel_lvl    = "OK"

        self.state          = STATE_IDLE
        self.current_target = None
        self.current_order  = None
        self._refuel_ticks  = 0

        self.total_fuel_used   = 0.0
        self.deliveries_made   = 0

    def move(self, engine: "RouteEngine | None") -> "str | None":
        completed_order_id = None

        if self.state == STATE_STOPPED:
            self.speed = 0
            return None

        if self.state == STATE_REFUELING:
            completed_order_id = self._tick_refueling(engine)
            return completed_order_id

        if self.state == STATE_IDLE:
            self._pick_next_target(engine)
            return None

        if self.current_target is None or self._reached_target():
            if self.current_target is not None and self._reached_target():
                completed_order_id = self.current_order
                self.deliveries_made += 1
                self.current_order  = None
                self.current_target = None
            self._pick_next_target(engine)

        if self.state in (STATE_DRIVING, STATE_CRAWLING) and self.current_target is not None:
            self._move_towards(self.current_target.x, self.current_target.y)
            burned = FUEL_BURN
            self.fuel -= burned
            self.total_fuel_used += burned

        return completed_order_id

    def _pick_next_target(self, engine):
        if engine is None or not engine.has_orders():
            if engine is not None and not engine.has_orders():
                self.state = STATE_STOPPED
            else:
                self.state = STATE_IDLE
            return

        now_ts = int(datetime.now(timezone.utc).timestamp())

        if self.state == STATE_CRAWLING:
            self._start_refueling()
            return

        dest = engine.get_next_target(self.truck_id, self.x, self.y, self.fuel, now_ts)

        if dest.name != "BASE":
            self.current_target = dest
            self.current_order  = dest.order_id
            self.state          = STATE_DRIVING
        else:
            nearest = engine.get_nearest_target(self.x, self.y)
            if nearest.name == "BASE":
                self.state = STATE_STOPPED
            else:
                self.current_target = nearest
                self.current_order  = nearest.order_id
                self._start_refueling()

    def _start_refueling(self):
        self.state         = STATE_REFUELING
        self._refuel_ticks = REFUEL_TICKS
        self.speed         = 0

    def _tick_refueling(self, engine) -> "str | None":
        self._refuel_ticks -= 1
        if self._refuel_ticks > 0:
            return None

        self.fuel  = FUEL_CAPACITY
        self.speed = self.base_speed

        if engine is None or not engine.has_orders():
            self.state = STATE_STOPPED if engine else STATE_IDLE
            return None

        if self.current_target is not None:
            dist = math.hypot(self.x - self.current_target.x,
                              self.y - self.current_target.y)
            if dist <= self.fuel * 10.0:
                self.state = STATE_DRIVING
            else:
                self.state = STATE_CRAWLING
        else:
            now_ts = int(datetime.now(timezone.utc).timestamp())
            dest = engine.get_next_target(self.truck_id, self.x, self.y, self.fuel, now_ts)
            if dest.name != "BASE":
                self.current_target = dest
                self.current_order  = dest.order_id
                self.state          = STATE_DRIVING
            else:
                self.state = STATE_STOPPED

        return None

    def _reached_target(self) -> bool:
        if self.current_target is None:
            return False
        if self.state == STATE_CRAWLING:
            return self.fuel <= 0
        dist = math.hypot(self.x - self.current_target.x,
                          self.y - self.current_target.y)
        return dist < 0.05

    def _move_towards(self, target_x: float, target_y: float):
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.hypot(dx, dy)
        if dist == 0:
            return
        self.x += (dx / dist) * STEP_SIZE
        self.y += (dy / dist) * STEP_SIZE

    def fuel_status(self):
        if self.fuel <= 0:
            self.fuel     = 0
            self.fuel_lvl = "EMPTY"
        elif self.fuel <= 10:
            self.fuel_lvl = "LOW"
        else:
            self.fuel_lvl = "OK"

    def wake_up(self):
        if self.state == STATE_IDLE:
            self.state = STATE_DRIVING

    def get_data(self) -> TruckData:
        return TruckData(
            id=self.truck_id,
            speed=self.speed,
            lat=round(self.x, 6),
            lng=round(self.y, 6),
            fuel=round(self.fuel, 2),
            fuel_lvl=self.fuel_lvl,
            state=self.state,
            order_id=self.current_order,
            target=self.current_target.name if self.current_target else None,
        )