import { useState } from 'react'
import { dispatch as apiDispatch } from '../api'

export default function DispatchPanel({ trucks, orders }) {
  const availableTrucks = trucks.filter((t) => t.state !== 'STOPPED')
  const pendingOrders = orders.filter((o) => o.status === 'PENDING')

  const [truckId, setTruckId] = useState('')
  const [orderId, setOrderId] = useState('')
  const [msg, setMsg] = useState(null)
  const [loading, setLoading] = useState(false)

  const canDispatch = truckId && orderId && !loading

  async function handleDispatch(e) {
    e.preventDefault()
    if (!canDispatch) return

    setLoading(true)
    setMsg(null)
    try {
      const result = await apiDispatch(truckId, orderId)
      if (result.success) {
        setMsg({ ok: true, text: `Dispatched ${truckId} → ${orderId}` })
        setTruckId('')
        setOrderId('')
      } else {
        setMsg({ ok: false, text: result.reason ?? 'Dispatch failed' })
      }
    } catch (err) {
      setMsg({ ok: false, text: err.message })
    } finally {
      setLoading(false)
      setTimeout(() => setMsg(null), 3000)
    }
  }

  return (
    <div className="card">
      <div className="card-title">Manual Dispatch</div>
      <form onSubmit={handleDispatch}>
        <div className="dispatch-row">
          <div className="form-group">
            <label>Truck</label>
            <select value={truckId} onChange={(e) => setTruckId(e.target.value)}>
              <option value="">— select —</option>
              {availableTrucks.map((t) => (
                <option key={t.id} value={t.id}>
                  {t.id} ({t.state})
                </option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label>Order</label>
            <select value={orderId} onChange={(e) => setOrderId(e.target.value)}>
              <option value="">— select —</option>
              {pendingOrders.map((o) => (
                <option key={o.id} value={o.id}>
                  {o.id} · {o.city}
                </option>
              ))}
            </select>
          </div>
        </div>

        <button className="btn btn-success" type="submit" disabled={!canDispatch}>
          {loading ? 'Dispatching…' : 'Dispatch'}
        </button>

        {msg && (
          <div className={`form-message ${msg.ok ? 'ok' : 'err'}`}>{msg.text}</div>
        )}

        {pendingOrders.length === 0 && (
          <div className="empty-state" style={{ marginTop: 6 }}>No pending orders</div>
        )}
      </form>
    </div>
  )
}
