import { useEffect, useState } from 'react'
import api from '../utils/api'
import './Home.css'

const DARKIAL_IMAGES = [
  '/images/Nivel_0.png',
  '/images/Nivel_1.png',
  '/images/Nivel_2.png',
  '/images/Nivel_3.png',
  '/images/Nivel_4.png',
  '/images/Nivel_5.png',
  '/images/Nivel_6.png',
  '/images/Nivel_7.png',
]

const EVOLUTION_NAMES = [
  'Antes del Despertar',
  'Aprendiz Humano',
  'Iniciado',
  'Guerrero',
  'Élite Oscuro',
  'Señor de la Tormenta',
  'Guardián',
  'Darkial Absoluto',
]

export default function Home() {
  const [profile, setProfile] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [newWeight, setNewWeight] = useState('')
  const [saving, setSaving] = useState(false)
  const [toast, setToast] = useState(null)

  useEffect(() => {
    fetchProfile()
  }, [])

  async function fetchProfile() {
    try {
      const res = await api.get('/user/profile')
      setProfile(res.data)
    } catch {
      setError('No se pudo conectar con el servidor')
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
      fetchProfile()
    } catch {
      showToast('Error al registrar peso', 'error')
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <div className="home-loading">Cargando...</div>
  if (error) return <div className="home-error">{error}</div>

  const xpPercent = Math.min((profile.xp_current / profile.xp_needed) * 100, 100)
  const weightLost = ((profile.weight_initial ?? 105) - profile.weight_current).toFixed(1)
  const weightToGo = (profile.weight_current - profile.weight_goal).toFixed(1)
  const progressPercent = Math.min(
    (((profile.weight_initial ?? 105) - profile.weight_current) / ((profile.weight_initial ?? 105) - profile.weight_goal)) * 100, 100
  ).toFixed(0)

  return (
    <div className="home">
      {toast && <div className={`toast ${toast.type}`}>{toast.message}</div>}

      {/* Header */}
      <div className="home-header">
        <div className="home-title">HUNTER<span>APP</span></div>
        <div className="home-coins">🪙 {profile.coins}</div>
      </div>

      {/* Personaje */}
      <div className="character-section">
        <div className="character-state-name">{EVOLUTION_NAMES[profile.evolution_state]}</div>
        <img
          src={DARKIAL_IMAGES[profile.evolution_state]}
          alt="Darkial"
          className="character-image"
        />
        <div className="character-name">{profile.name}</div>
      </div>

      {/* Nivel y XP */}
      <div className="level-section">
        <div className="level-row">
          <span className="level-label">Nivel {profile.level}</span>
          <span className="level-xp">{profile.xp_current} / {profile.xp_needed} XP</span>
        </div>
        <div className="xp-bar-bg">
          <div className="xp-bar-fill" style={{ width: `${xpPercent}%` }} />
        </div>
      </div>

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
      <div className="weight-progress-card">
        <div className="quick-stats">
          <div className="stat-card">
            <div className="stat-value">{profile.weight_current} kg</div>
            <div className="stat-label">Peso actual</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{weightLost} kg</div>
            <div className="stat-label">Perdidos</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{weightToGo} kg</div>
            <div className="stat-label">Para la meta</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">🔥 {profile.streak_days}</div>
            <div className="stat-label">Racha</div>
          </div>
        </div>
        <div className="progress-label-row">
          <span>Progreso total</span>
          <span>{progressPercent}%</span>
        </div>
        <div className="progress-bar-bg">
          <div className="progress-bar-fill" style={{ width: `${progressPercent}%` }} />
        </div>
      </div>

      {/* Días activos */}
      <div className="active-days">
        <span>⚡ {profile.active_days_total} días activos acumulados</span>
      </div>
    </div>
  )
}