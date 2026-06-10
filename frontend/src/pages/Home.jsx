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

  useEffect(() => {
    api.get('/user/profile')
      .then(res => setProfile(res.data))
      .catch(() => setError('No se pudo conectar con el servidor'))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="home-loading">Cargando...</div>
  if (error) return <div className="home-error">{error}</div>

  const xpPercent = Math.min((profile.xp_current / profile.xp_needed) * 100, 100)
  const weightLost = ((profile.weight_initial ?? 105) - profile.weight_current).toFixed(1)
  const weightToGo = (profile.weight_current - profile.weight_goal).toFixed(1)

  return (
    <div className="home">
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

      {/* Stats rápidos */}
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

      {/* Días activos */}
      <div className="active-days">
        <span>⚡ {profile.active_days_total} días activos acumulados</span>
      </div>
    </div>
  )
}