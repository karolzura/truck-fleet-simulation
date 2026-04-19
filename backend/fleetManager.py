import uuid
from typing import List, Optional, Dict, Set
from datetime import datetime, timezone
 
from trucks import Truck, STATE_STOPPED, STATE_IDLE
from model import TruckData, Order, FleetMetrics, Alert
 
TRUCK_COUNT = 5
TRUCK_SPEED = 60
TRUCK_FUEL  = 100.0
 
 
class FleetManager:
    def __init__(self):
        self.trucks: List[Truck]      = []
        self.orders: Dict[str, Order] = {}
        self.alerts: List[Alert]      = []
        self.engine                   = None
        self._id_counter              = 0
        self._alerted_orders: Set[str] = set()
        self._delivery_fuel_samples: List[float] = []
 
        self._init_engine()
        self._spawn_fleet()
 
    def _init_engine(self):
        try:
            from simulation_engine import RouteEngine
            self.engine = RouteEngine()
        except ImportError:
            self.engine = None
 
    def _spawn_fleet(self):
        for _ in range(TRUCK_COUNT):
            truck_id = f"TRUCK-{self._id_counter:02d}"
            self._id_counter += 1
            self.trucks.append(Truck(truck_id, speed=TRUCK_SPEED, fuel=TRUCK_FUEL))
 
    def add_order(self, city: str, lat: float, lng: float,
                  priority: int, deadline: datetime) -> Order:
        order_id    = str(uuid.uuid4())[:8].upper()
        deadline_ts = int(deadline.astimezone(timezone.utc).timestamp())
 
        order = Order(
            id=order_id,
            city=city,
            lat=lat,
            lng=lng,
            priority=priority,
            deadline=deadline,
        )
        self.orders[order_id] = order
 
        if self.engine:
            self.engine.add_order(order_id, city, lat, lng, priority, deadline_ts)
 
        for truck in self.trucks:
            if truck.state == STATE_IDLE:
                truck.wake_up()
 
        return order
 
    def dispatch(self, truck_id: str, order_id: str) -> dict:
        truck = next((t for t in self.trucks if t.truck_id == truck_id), None)
        if truck is None:
            return {"success": False, "reason": f"Truck {truck_id} not found"}
 
        order = self.orders.get(order_id)
        if order is None:
            return {"success": False, "reason": f"Order {order_id} not found"}
 
        if order.status != "PENDING":
            return {"success": False, "reason": f"Order {order_id} is already {order.status}"}
 
        if truck.state == STATE_STOPPED:
            return {"success": False, "reason": f"Truck {truck_id} is stopped"}
 
        if self.engine is None:
            return {"success": False, "reason": "Routing engine unavailable"}
 
        now_ts = int(datetime.now(timezone.utc).timestamp())
        ok = self.engine.assign_order(truck_id, order_id, truck.x, truck.y, truck.fuel, now_ts)
 
        if not ok:
            import math
            dist   = math.hypot(truck.x - order.lat, truck.y - order.lng)
            reason = (
                f"Order {order_id} out of fuel range "
                f"(distance {dist:.2f} deg, fuel {truck.fuel:.1f})"
            )
            return {"success": False, "reason": reason}
 
        if truck.current_order:
            old = self.orders.get(truck.current_order)
            if old:
                old.status      = "PENDING"
                old.assigned_to = None
                self.engine.add_order(
                    old.id, old.city, old.lat, old.lng,
                    old.priority,
                    int(old.deadline.astimezone(timezone.utc).timestamp()),
                )
 
        class _FakeDest:
            def __init__(self, o: Order):
                self.name        = o.city
                self.order_id    = o.id
                self.x           = o.lat
                self.y           = o.lng
                self.priority    = o.priority
                self.deadline_ts = int(o.deadline.astimezone(timezone.utc).timestamp())
                self.visited     = True
 
        truck.current_target = _FakeDest(order)
        truck.current_order  = order_id
        truck.state          = "DRIVING"
        order.status         = "IN_PROGRESS"
        order.assigned_to    = truck_id
 
        return {"success": True, "reason": f"Truck {truck_id} manually assigned to order {order_id}"}
 
    async def update_all(self):
        now    = datetime.now(timezone.utc)
        now_ts = int(now.timestamp())
 
        for truck in self.trucks:
            completed_order_id = truck.move(self.engine)
            truck.fuel_status()
 
            if completed_order_id:
                self._on_delivery(completed_order_id, truck, now)
 
            if truck.current_order:
                order = self.orders.get(truck.current_order)
                if order and order.status == "PENDING":
                    order.status      = "IN_PROGRESS"
                    order.assigned_to = truck.truck_id
 
        self._check_deadline_alerts(now_ts, now)
 
    def _on_delivery(self, order_id: str, truck: Truck, now: datetime):
        order = self.orders.get(order_id)
        if order is None:
            return
 
        order.delivered_at = now
        deadline_ts        = int(order.deadline.astimezone(timezone.utc).timestamp())
        on_time            = int(now.timestamp()) <= deadline_ts
        order.status       = "DELIVERED_ON_TIME" if on_time else "DELIVERED_LATE"
 
        if truck.deliveries_made > 0:
            fuel_per_delivery = truck.total_fuel_used / truck.deliveries_made
            self._delivery_fuel_samples.append(fuel_per_delivery)
 
        if not on_time:
            self._push_alert(
                truck_id=truck.truck_id,
                order_id=order_id,
                level="WARNING",
                message=f"Order {order_id} delivered late to {order.city}",
                now=now,
            )
 
    def _check_deadline_alerts(self, now_ts: int, now: datetime):
        for order in self.orders.values():
            if order.status not in ("PENDING", "IN_PROGRESS"):
                continue
            if order.id in self._alerted_orders:
                continue
            deadline_ts = int(order.deadline.astimezone(timezone.utc).timestamp())
            if deadline_ts - now_ts < 60 and order.status == "PENDING":
                self._alerted_orders.add(order.id)
                self._push_alert(
                    truck_id=None,
                    order_id=order.id,
                    level="CRITICAL",
                    message=f"Order {order.id} ({order.city}) deadline in <60s — unassigned",
                    now=now,
                )
 
    def _push_alert(self, truck_id, order_id, level, message, now):
        self.alerts.append(Alert(
            truck_id=truck_id,
            order_id=order_id,
            level=level,
            message=message,
            timestamp=now,
        ))
        if len(self.alerts) > 200:
            self.alerts = self.alerts[-200:]
 
    def get_metrics(self) -> FleetMetrics:
        total     = len(self.orders)
        on_time   = sum(1 for o in self.orders.values() if o.status == "DELIVERED_ON_TIME")
        late      = sum(1 for o in self.orders.values() if o.status == "DELIVERED_LATE")
        pending   = sum(1 for o in self.orders.values() if o.status == "PENDING")
        in_prog   = sum(1 for o in self.orders.values() if o.status == "IN_PROGRESS")
        delivered = on_time + late
        on_time_rate = (on_time / delivered * 100.0) if delivered > 0 else 0.0
        avg_fuel = (
            sum(self._delivery_fuel_samples) / len(self._delivery_fuel_samples)
            if self._delivery_fuel_samples else 0.0
        )
        return FleetMetrics(
            total_orders=total,
            delivered_on_time=on_time,
            delivered_late=late,
            pending=pending,
            in_progress=in_prog,
            on_time_rate=round(on_time_rate, 1),
            avg_fuel_per_delivery=round(avg_fuel, 2),
        )
 
    def get_fleet_data(self) -> List[TruckData]:
        return [t.get_data() for t in self.trucks]
 
    def get_orders(self) -> List[Order]:
        return list(self.orders.values())
 
    def get_alerts(self, limit: int = 50) -> List[Alert]:
        return self.alerts[-limit:]
 
    def add_truck(self) -> TruckData:
        truck_id = f"TRUCK-{self._id_counter:02d}"
        self._id_counter += 1
        truck = Truck(truck_id, speed=TRUCK_SPEED, fuel=TRUCK_FUEL)
        self.trucks.append(truck)
        return truck.get_data()
 
    def remove_truck(self, truck_id: str) -> bool:
        before       = len(self.trucks)
        self.trucks  = [t for t in self.trucks if t.truck_id != truck_id]
        return len(self.trucks) < before
 
    def get_truck(self, truck_id: str) -> Optional[TruckData]:
        truck = next((t for t in self.trucks if t.truck_id == truck_id), None)
        return truck.get_data() if truck else None
 