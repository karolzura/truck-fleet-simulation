import { useState } from 'react'
import { POLISH_CITIES } from '../constants'
import { createOrder } from '../api'

function defaultDeadline() {
  return new Date(Date.now() + 2 * 3600 * 1000).toISOString().slice(0, 16)
}

export default function OrderForm() {
  const [city, setCity] = useState(POLISH_CITIES[0].name)
  const [priority, setPriority] = useState(5)
  const [deadline, setDeadline] = useState(defaultDeadline)
  const [msg, setMsg] = useState(null)
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    const cityData = POLISH_CITIES.find((c) => c.name === city)
    if (!cityData) return

    setLoading(true)
    setMsg(null)
    try {
      await createOrder({
        city: cityData.name,
        lat: cityData.lat,
        lng: cityData.lng,
        priority: Number(priority),
        deadline: new Date(deadline).toISOString(),
      })
      setMsg({ ok: true, text: `Order created → ${city}` })
      setCity(POLISH_CITIES[0].name)
      setPriority(5)
      setDeadline(defaultDeadline())
    } catch (err) {
      setMsg({ ok: false, text: err.message })
    } finally {
      setLoading(false)
      setTimeout(() => setMsg(null), 3000)
    }
  }

  return (
    <div className="card">
      <div className="card-title">New Order</div>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Destination</label>
          <select value={city} onChange={(e) => setCity(e.target.value)}>
            {POLISH_CITIES.map((c) => (
              <option key={c.name} value={c.name}>{c.name}</option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label>Priority: {priority}</label>
          <input
            type="range"
            min={1}
            max={10}
            value={priority}
            onChange={(e) => setPriority(e.target.value)}
          />
        </div>

        <div className="form-group">
          <label>Deadline</label>
          <input
            type="datetime-local"
            value={deadline}
            onChange={(e) => setDeadline(e.target.value)}
            required
          />
        </div>

        <button className="btn btn-primary" type="submit" disabled={loading}>
          {loading ? 'Creating…' : 'Create Order'}
        </button>

        {msg && (
          <div className={`form-message ${msg.ok ? 'ok' : 'err'}`}>{msg.text}</div>
        )}
      </form>
    </div>
  )
}
