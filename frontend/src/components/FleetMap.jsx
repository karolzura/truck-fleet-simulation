import { MapContainer, TileLayer, CircleMarker, Marker, Popup } from 'react-leaflet'
import L from 'leaflet'
import iconUrl from 'leaflet/dist/images/marker-icon.png'
import iconRetinaUrl from 'leaflet/dist/images/marker-icon-2x.png'
import shadowUrl from 'leaflet/dist/images/marker-shadow.png'
import { TRUCK_STATE_COLORS } from '../constants'

delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({ iconUrl, iconRetinaUrl, shadowUrl })

const POLAND_CENTER = [52.1, 19.4]
const ACTIVE_ORDER_STATUSES = new Set(['PENDING', 'IN_PROGRESS'])

function deadlineLabel(deadline) {
  const diff = Math.floor((new Date(deadline) - Date.now()) / 1000)
  if (diff < 0) return 'OVERDUE'
  const m = Math.floor(diff / 60)
  const s = diff % 60
  return `${m}m ${s}s`
}

export default function FleetMap({ trucks, orders }) {
  const activeOrders = orders.filter((o) => ACTIVE_ORDER_STATUSES.has(o.status))

  return (
    <MapContainer
      center={POLAND_CENTER}
      zoom={6}
      style={{ height: '100%', width: '100%', background: '#0f1117' }}
      zoomControl={true}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
      />

      {trucks.map((truck) => (
        <CircleMarker
          key={truck.id}
          center={[truck.lat, truck.lng]}
          radius={10}
          pathOptions={{
            fillColor: TRUCK_STATE_COLORS[truck.state] ?? '#6b7280',
            fillOpacity: 0.9,
            color: '#0f1117',
            weight: 2,
          }}
        >
          <Popup>
            <strong>{truck.id}</strong><br />
            State: {truck.state}<br />
            Fuel: {truck.fuel.toFixed(0)}% ({truck.fuel_lvl})<br />
            {truck.target && <>Target: {truck.target}<br /></>}
            {truck.order_id && <>Order: {truck.order_id}</>}
          </Popup>
        </CircleMarker>
      ))}

      {activeOrders.map((order) => (
        <Marker key={order.id} position={[order.lat, order.lng]}>
          <Popup>
            <strong>{order.city}</strong><br />
            Priority: {order.priority}<br />
            Status: {order.status}<br />
            Deadline: {deadlineLabel(order.deadline)}<br />
            {order.assigned_to && <>Assigned: {order.assigned_to}</>}
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  )
}
