import { useEffect, useState } from 'react'
import api from '../utils/api'
import './Config.css'

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

export default function Config() {
  const [profile, setProfile] = useState(null)
  const [loading, setLoading] = useState(true)
  const [toast, setToast] = useState(null)

  useEffect(() => {
    api.get('/user/profile')
      .then(res => setProfile(res.data))
      .finally(() => setLoading(false))
  }, [])

  function showToast(message, type = 'success') {
    setToast({ message, type })
    setTimeout(() => setToast(null), 3000)
  }

  if (loading) return <div className="config-loading">Cargando...</div>

  return (
    <div className="config">
      {toast && <div className={`toast ${toast.type}`}>{toast.message}</div>}

      <h1 className="config-title">Configuración</h1>

      {/* Perfil */}
      <div className="config-card">
        <div className="config-card-title">👤 Perfil</div>
        <div className="config-row">
          <span className="config-label">Nombre</span>
          <span className="config-value">{profile.name}</span>
        </div>
        <div className="config-row">
          <span className="config-label">Estatura</span>
          <span className="config-value">{profile.height_cm} cm</span>
        </div>
        <div className="config-row">
          <span className="config-label">Peso inicial</span>
          <span className="config-value">105 kg</span>
        </div>
        <div className="config-row">
          <span className="config-label">Peso meta</span>
          <span className="config-value">{profile.weight_goal} kg</span>
        </div>
      </div>

      {/* Estado actual */}
      <div className="config-card">
        <div className="config-card-title">⚔️ Estado actual</div>
        <div className="config-row">
          <span className="config-label">Nivel</span>
          <span className="config-value highlight">{profile.level}</span>
        </div>
        <div className="config-row">
          <span className="config-label">Evolución</span>
          <span className="config-value highlight">{EVOLUTION_NAMES[profile.evolution_state]}</span>
        </div>
        <div className="config-row">
          <span className="config-label">XP total</span>
          <span className="config-value">{profile.xp_total}</span>
        </div>
        <div className="config-row">
          <span className="config-label">Monedas</span>
          <span className="config-value">🪙 {profile.coins}</span>
        </div>
        <div className="config-row">
          <span className="config-label">Racha</span>
          <span className="config-value">🔥 {profile.streak_days} días</span>
        </div>
        <div className="config-row">
          <span className="config-label">Días activos</span>
          <span className="config-value">⚡ {profile.active_days_total}</span>
        </div>
        <div className="config-row">
          <span className="config-label">Puntos de falla (semana)</span>
          <span className={`config-value ${profile.fault_points_week >= 3 ? 'danger' : ''}`}>
            {profile.fault_points_week} / 5
          </span>
        </div>
        <div className="config-row">
          <span className="config-label">Escudo disponible</span>
          <span className="config-value">{profile.shield_available ? '🛡️ Sí' : '❌ No'}</span>
        </div>
      </div>

      {/* Sistema */}
      <div className="config-card">
        <div className="config-card-title">⚙️ Sistema</div>
        <div className="config-row">
          <span className="config-label">Versión</span>
          <span className="config-value">HunterAPP v1.0</span>
        </div>
        <div className="config-row">
          <span className="config-label">Backend</span>
          <span className="config-value">FastAPI + PostgreSQL</span>
        </div>
        <div className="config-row">
          <span className="config-label">Dominio</span>
          <span className="config-value">hunter.lukifix.mx</span>
        </div>
      </div>

      {/* Fórmula XP */}
      <div className="config-card">
        <div className="config-card-title">📐 Fórmula de XP</div>
        <div className="formula">XP(N) = 500 × N × 1.15^(N-1)</div>
        <div className="config-row">
          <span className="config-label">Nivel {profile.level} → {profile.level + 1}</span>
          <span className="config-value highlight">{profile.xp_needed} XP</span>
        </div>
        <div className="config-row">
          <span className="config-label">XP actual</span>
          <span className="config-value">{profile.xp_current} / {profile.xp_needed}</span>
        </div>
      </div>
    </div>
  )
}