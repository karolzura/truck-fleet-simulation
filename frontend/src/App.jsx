import { useState, useEffect } from 'react'
import 'leaflet/dist/leaflet.css'
import './App.css'
import * as api from './api'
import MetricsBar from './components/MetricsBar'
import FleetMap from './components/FleetMap'
import FleetSidebar from './components/FleetSidebar'
import OrderForm from './components/OrderForm'
import DispatchPanel from './components/DispatchPanel'
import AlertsFeed from './components/AlertsFeed'

export default function App() {
  const [trucks, setTrucks] = useState([])
  const [orders, setOrders] = useState([])
  const [metrics, setMetrics] = useState(null)
  const [alerts, setAlerts] = useState([])

  useEffect(() => {
    const poll = async () => {
      try {
        const [t, o, m, a] = await Promise.all([
          api.getFleet(),
          api.getOrders(),
          api.getMetrics(),
          api.getAlerts(),
        ])
        setTrucks(t)
        setOrders(o)
        setMetrics(m)
        setAlerts(a)
      } catch (err) {
        console.error('Poll error:', err)
      }
    }
    poll()
    const id = setInterval(poll, 2000)
    return () => clearInterval(id)
  }, [])

  return (
    <div className="app-layout">
      <MetricsBar metrics={metrics} trucksCount={trucks.length} />
      <div className="map-area">
        <FleetMap trucks={trucks} orders={orders} />
      </div>
      <div className="right-panel">
        <FleetSidebar trucks={trucks} />
        <OrderForm />
        <DispatchPanel trucks={trucks} orders={orders} />
        <AlertsFeed alerts={alerts} />
      </div>
    </div>
  )
}
