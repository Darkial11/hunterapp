import { useEffect, useState } from 'react'
import api from '../utils/api'
import './Stats.css'

export default function Stats() {
  const [profile, setProfile] = useState(null)
  const [history, setHistory] = useState([])
  const [newWeight, setNewWeight] = useState('')
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [toast, setToast] = useState(null)

  useEffect(() => {
    fetchData()
  }, [])

  async function fetchData() {
    try {
      const [prof, hist] = await Promise.all([
        api.get('/user/profile'),
        api.get('/user/weight/history'),
      ])
      setProfile(prof.data)
      setHistory(hist.data)
    } catch {
      showToast('Error al cargar datos', 'error')
    } finally {
      setLoading(false)
    }
  }

  function showToast(message, type = 'success') {
    setToast({ message, type })
    setTimeout(() => setToast(null), 3000)
  }

  async function logWeight() {
    const kg = parseFloat(newWeight)
    if (isNaN(kg) || kg < 40 || kg > 200) {
      showToast('Ingresa un peso válido', 'error')
      return
    }
    setSaving(true)
    try {
      await api.post(`/user/weight?weight_kg=${kg}`)
      showToast('Peso registrado ✓')
      setNewWeight('')
      fetchData()
    } catch {
      showToast('Error al registrar peso', 'error')
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <div className="stats-loading">Cargando...</div>

  const imc = (profile.weight_current / ((profile.height_cm / 100) ** 2)).toFixed(1)
  const weightLost = (105 - profile.weight_current).toFixed(1)
  const weightToGo = (profile.weight_current - profile.weight_goal).toFixed(1)
  const progressPercent = Math.min(
    ((105 - profile.weight_current) / (105 - profile.weight_goal)) * 100, 100
  ).toFixed(0)

  // Últimos 7 registros para la mini gráfica
  const recent = history.slice(-7)
  const maxW = recent.length > 0 ? Math.max(...recent.map(r => r.weight_kg)) : 105
  const minW = recent.length > 0 ? Math.min(...recent.map(r => r.weight_kg)) : 85

  return (
    <div className="stats">
      {toast && <div className={`toast ${toast.type}`}>{toast.message}</div>}

      <h1 className="stats-title">Estadísticas</h1>

      {/* Registrar peso */}
      <div className="weight-input-card">
        <div className="weight-input-label">Registrar peso de hoy</div>
        <div className="weight-input-row">
          <input
            type="number"
            step="0.1"
            placeholder="ej. 104.5"
            value={newWeight}
            onChange={e => setNewWeight(e.target.value)}
            className="weight-input"
          />
          <button
            className="weight-save-btn"
            onClick={logWeight}
            disabled={saving}
          >
            {saving ? '...' : 'Guardar'}
          </button>
        </div>
      </div>

      {/* Progreso de peso */}
      <div className="stats-card">
        <div className="stats-card-title">⚖️ Progreso de peso</div>
        <div className="weight-stats-grid">
          <div className="weight-stat">
            <div className="weight-stat-value">{profile.weight_current} kg</div>
            <div className="weight-stat-label">Actual</div>
          </div>
          <div className="weight-stat">
            <div className="weight-stat-value highlight">{weightLost} kg</div>
            <div className="weight-stat-label">Perdidos</div>
          </div>
          <div className="weight-stat">
            <div className="weight-stat-value">{weightToGo} kg</div>
            <div className="weight-stat-label">Para la meta</div>
          </div>
          <div className="weight-stat">
            <div className="weight-stat-value">{profile.weight_goal} kg</div>
            <div className="weight-stat-label">Meta</div>
          </div>
        </div>

        <div className="progress-label-row">
          <span>Progreso total</span>
          <span>{progressPercent}%</span>
        </div>
        <div className="progress-bar-bg">
          <div className="progress-bar-fill" style={{ width: `${progressPercent}%` }} />
        </div>

        {/* Mini gráfica */}
        {recent.length > 1 && (
          <div className="mini-chart">
            {recent.map((r, i) => {
              const range = maxW - minW || 1
              const heightPct = 100 - ((r.weight_kg - minW) / range) * 80
              return (
                <div key={i} className="chart-bar-col">
                  <div
                    className="chart-bar"
                    style={{ height: `${heightPct}%` }}
                  />
                  <div className="chart-label">{r.weight_kg}</div>
                  <div className="chart-date">
                    {r.date.slice(5)}
                  </div>
                </div>
              )
            })}
          </div>
        )}

        {recent.length === 0 && (
          <div className="no-data">Aún no hay registros de peso</div>
        )}
      </div>

      {/* IMC */}
      <div className="stats-card">
        <div className="stats-card-title">📏 IMC</div>
        <div className="imc-value">{imc}</div>
        <div className="imc-label">
          {imc < 18.5 ? 'Bajo peso' :
           imc < 25 ? '✅ Peso normal' :
           imc < 30 ? 'Sobrepeso' : 'Obesidad'}
        </div>
        <div className="imc-meta">Meta: ~25.7 (peso normal)</div>
      </div>

      {/* Racha y días activos */}
      <div className="stats-card">
        <div className="stats-card-title">🔥 Actividad</div>
        <div className="activity-grid">
          <div className="activity-stat">
            <div className="activity-value">{profile.streak_days}</div>
            <div className="activity-label">Racha actual (días)</div>
          </div>
          <div className="activity-stat">
            <div className="activity-value">{profile.active_days_total}</div>
            <div className="activity-label">Días activos totales</div>
          </div>
          <div className="activity-stat">
            <div className="activity-value">{profile.level}</div>
            <div className="activity-label">Nivel actual</div>
          </div>
          <div className="activity-stat">
            <div className="activity-value">{profile.xp_total}</div>
            <div className="activity-label">XP total ganado</div>
          </div>
        </div>
      </div>
    </div>
  )
}