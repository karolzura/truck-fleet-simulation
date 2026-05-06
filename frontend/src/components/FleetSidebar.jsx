import { TRUCK_STATE_COLORS, FUEL_LVL_COLORS } from '../constants'

export default function FleetSidebar({ trucks }) {
  return (
    <div className="card">
      <div className="card-title">Fleet ({trucks.length} trucks)</div>
      {trucks.length === 0 && <div className="empty-state">No trucks</div>}
      {trucks.map((truck) => (
        <TruckCard key={truck.id} truck={truck} />
      ))}
    </div>
  )
}

function TruckCard({ truck }) {
  const stateColor = TRUCK_STATE_COLORS[truck.state] ?? '#6b7280'
  const fuelColor = FUEL_LVL_COLORS[truck.fuel_lvl] ?? '#22c55e'
  const fuelPct = Math.min(100, Math.max(0, truck.fuel))

  return (
    <div className="truck-card">
      <div className="truck-header">
        <span className="truck-id">{truck.id}</span>
        <span className="state-badge" style={{ background: `${stateColor}22`, color: stateColor }}>
          <span className="state-dot" style={{ background: stateColor }} />
          {truck.state}
        </span>
      </div>

      <div className="fuel-bar-container">
        <div
          className="fuel-bar-fill"
          style={{ width: `${fuelPct}%`, background: fuelColor }}
        />
      </div>

      <div className="truck-detail">
        {truck.target
          ? `→ ${truck.target}`
          : truck.state === 'IDLE'
          ? 'Waiting for order'
          : truck.state === 'REFUELING'
          ? 'Refueling at base'
          : '—'}
        {' '}
        <span style={{ color: fuelColor }}>⬟ {truck.fuel.toFixed(0)}%</span>
      </div>
    </div>
  )
}
