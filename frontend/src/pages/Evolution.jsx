import { useEffect, useState } from 'react'
import api from '../utils/api'
import './Evolution.css'

const EVOLUTION_STATES = [
  {
    id: 0,
    name: 'Antes del Despertar',
    levels: 'Inicio',
    description: 'El punto de partida. Darkial despierta.',
    image: '/images/Nivel_0.png',
    condition: null,
  },
  {
    id: 1,
    name: 'Aprendiz Humano',
    levels: 'Niveles 1-10',
    description: 'Sin poderes, sin aura. El camino comienza.',
    image: '/images/Nivel_1.png',
    condition: null,
  },
  {
    id: 2,
    name: 'Iniciado',
    levels: 'Niveles 11-20',
    description: 'Más musculoso. El cuerpo empieza a cambiar.',
    image: '/images/Nivel_2.png',
    condition: { days: 7, weight: 102 },
  },
  {
    id: 3,
    name: 'Guerrero',
    levels: 'Niveles 21-35',
    description: 'Aura azul eléctrica. Ojos azules. El poder despierta.',
    image: '/images/Nivel_3.png',
    condition: { days: 30, weight: 99 },
  },
  {
    id: 4,
    name: 'Élite Oscuro',
    levels: 'Niveles 36-55',
    description: 'Gabardina oscura con relámpagos azules.',
    image: '/images/Nivel_4.png',
    condition: { days: 60, weight: 95 },
  },
  {
    id: 5,
    name: 'Señor de la Tormenta',
    levels: 'Niveles 56-75',
    description: 'Gabardina con runas azules. Aura controlada y limpia.',
    image: '/images/Nivel_5.png',
    condition: { days: 90, weight: 91 },
  },
  {
    id: 6,
    name: 'Guardián',
    levels: 'Niveles 76-90',
    description: 'Aura azul limpia. Sombras oscuras a su alrededor.',
    image: '/images/Nivel_6.png',
    condition: { days: 120, weight: 88 },
  },
  {
    id: 7,
    name: 'Darkial Absoluto',
    levels: 'Niveles 91-100',
    description: 'La forma final. Capucha nórdica, tentáculos de sombra, llamas azules y moradas.',
    image: '/images/Nivel_7.png',
    condition: { days: 150, weight: 85 },
  },
]

export default function Evolution() {
  const [profile, setProfile] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/user/profile')
      .then(res => setProfile(res.data))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="evo-loading">Cargando...</div>

  const currentState = profile.evolution_state

  return (
    <div className="evolution">
      <h1 className="evo-title">Evolución de Darkial</h1>
      <div className="evo-current-label">
        Estado actual: <span>{EVOLUTION_STATES[currentState].name}</span>
      </div>

      <div className="evo-list">
        {EVOLUTION_STATES.map(state => {
          const isUnlocked = currentState >= state.id
          const isCurrent = currentState === state.id

          let conditionText = null
          if (state.condition && !isUnlocked) {
            const daysLeft = Math.max(0, state.condition.days - profile.active_days_total)
            const weightLeft = Math.max(0, profile.weight_current - state.condition.weight).toFixed(1)
            conditionText = `${daysLeft} días activos + bajar ${weightLeft} kg más`
          }

          return (
            <div
              key={state.id}
              className={`evo-card ${isUnlocked ? 'unlocked' : 'locked'} ${isCurrent ? 'current' : ''}`}
            >
              <div className="evo-image-container">
                {isUnlocked ? (
                  <img src={state.image} alt={state.name} className="evo-image" />
                ) : (
                  <div className="evo-locked-image">🔒</div>
                )}
                {isCurrent && <div className="evo-current-badge">ACTUAL</div>}
              </div>
              <div className="evo-info">
                <div className="evo-name">{state.name}</div>
                <div className="evo-levels">{state.levels}</div>
                <div className="evo-desc">{state.description}</div>
                {conditionText && (
                  <div className="evo-condition">⚡ Falta: {conditionText}</div>
                )}
                {isUnlocked && !isCurrent && (
                  <div className="evo-done">✓ Completado</div>
                )}
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}