import { API_BASE } from './constants'

async function request(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, options)
  if (!res.ok) {
    const text = await res.text()
    throw new Error(`${res.status} ${text}`)
  }
  if (res.status === 204) return null
  return res.json()
}

export const getFleet = () => request('/fleet')

export const getOrders = (status) =>
  request('/orders' + (status ? `?status=${status}` : ''))

export const getMetrics = () => request('/metrics')

export const getAlerts = (limit = 50) => request(`/alerts?limit=${limit}`)

export const createOrder = (payload) =>
  request('/orders', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })

export const dispatch = (truck_id, order_id) =>
  request('/dispatch', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ truck_id, order_id }),
  })

export const addTruck = () => request('/fleet', { method: 'POST' })

export const removeTruck = (truck_id) =>
  request(`/fleet/${truck_id}`, { method: 'DELETE' })
