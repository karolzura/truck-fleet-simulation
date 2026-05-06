function rateColor(rate) {
  if (rate >= 80) return 'green'
  if (rate >= 50) return 'yellow'
  return 'red'
}

export default function MetricsBar({ metrics, trucksCount }) {
  const kpis = metrics
    ? [
        { label: 'Trucks', value: trucksCount },
        { label: 'Total Orders', value: metrics.total_orders },
        { label: 'Pending', value: metrics.pending },
        { label: 'In Progress', value: metrics.in_progress },
        { label: 'On Time', value: metrics.delivered_on_time },
        { label: 'Late', value: metrics.delivered_late },
        {
          label: 'On-Time Rate',
          value: `${metrics.on_time_rate.toFixed(1)}%`,
          colorClass: rateColor(metrics.on_time_rate),
        },
        {
          label: 'Avg Fuel/Delivery',
          value: metrics.avg_fuel_per_delivery.toFixed(1),
        },
      ]
    : []

  return (
    <div className="metrics-bar">
      <span style={{ fontSize: 13, fontWeight: 700, color: '#6b7280', marginRight: 8, flexShrink: 0 }}>
        FLEET DASHBOARD
      </span>
      {kpis.length === 0 ? (
        <span style={{ fontSize: 12, color: '#4b5563' }}>Connecting to backend…</span>
      ) : (
        kpis.map((k) => (
          <div className="kpi-card" key={k.label}>
            <span className="kpi-label">{k.label}</span>
            <span className={`kpi-value ${k.colorClass ?? ''}`}>{k.value}</span>
          </div>
        ))
      )}
    </div>
  )
}
