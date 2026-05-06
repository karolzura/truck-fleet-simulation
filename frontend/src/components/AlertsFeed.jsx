function formatTime(ts) {
  return new Date(ts).toLocaleTimeString('pl-PL', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  })
}

export default function AlertsFeed({ alerts }) {
  const sorted = [...alerts].reverse()

  return (
    <div className="card">
      <div className="card-title">Alerts ({alerts.length})</div>
      {sorted.length === 0 ? (
        <div className="empty-state">No alerts</div>
      ) : (
        <div className="alerts-scroll">
          {sorted.map((alert, i) => (
            <div key={i} className={`alert-item ${alert.level}`}>
              <div className="alert-level">{alert.level}</div>
              <div className="alert-message">{alert.message}</div>
              <div className="alert-time">{formatTime(alert.timestamp)}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
