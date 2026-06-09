import { useEffect, useState } from 'react'
import api from '../utils/api'
import './Achievements.css'

const ACHIEVEMENT_ICONS = {
  weight: '⚖️',
  streak: '🔥',
  missions: '📋',
  legendary: '👑',
}

export default function Achievements() {
  const [achievements, setAchievements] = useState([])
  const [unlocked, setUnlocked] = useState([])
  const [profile, setProfile] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchData()
  }, [])

  async function fetchData() {
    try {
      const prof = await api.get('/user/profile')
      setProfile(prof.data)

      // Por ahora cargamos el catálogo directo desde el backend
      // En el siguiente paso agregamos el endpoint de logros
      setAchievements([
        { id: 1, name: 'Primer kilo perdido', description: 'Registrar 104 kg', achievement_type: 'weight', condition_value: 104, xp_reward: 100, is_legendary: false },
        { id: 2, name: 'Hito 100 kg', description: 'Llegar a 100 kg', achievement_type: 'weight', condition_value: 100, xp_reward: 300, is_legendary: false },
        { id: 3, name: 'Hito 95 kg', description: 'Llegar a 95 kg', achievement_type: 'weight', condition_value: 95, xp_reward: 500, is_legendary: false },
        { id: 4, name: 'Hito 90 kg', description: 'Llegar a 90 kg', achievement_type: 'weight', condition_value: 90, xp_reward: 800, is_legendary: false },
        { id: 5, name: 'Darkial Absoluto', description: 'Llegar a 85 kg — meta final', achievement_type: 'weight', condition_value: 85, xp_reward: 2000, is_legendary: true },
        { id: 6, name: 'Primera semana', description: '7 días activos consecutivos', achievement_type: 'streak', condition_value: 7, xp_reward: 150, is_legendary: false },
        { id: 7, name: 'Mes completo', description: '30 días activos consecutivos', achievement_type: 'streak', condition_value: 30, xp_reward: 400, is_legendary: false },
        { id: 8, name: '100 días activos', description: '100 días activos acumulados', achievement_type: 'streak', condition_value: 100, xp_reward: 800, is_legendary: false },
        { id: 9, name: '150 días activos', description: '150 días activos acumulados', achievement_type: 'streak', condition_value: 150, xp_reward: 1200, is_legendary: false },
        { id: 10, name: 'Día perfecto', description: 'Completar todas las misiones del día', achievement_type: 'missions', condition_value: 1, xp_reward: 50, is_legendary: false },
        { id: 11, name: '10 días perfectos', description: 'Acumular 10 días perfectos', achievement_type: 'missions', condition_value: 10, xp_reward: 300, is_legendary: false },
        { id: 12, name: 'Conocimiento total', description: 'Completar 50 misiones de conocimiento', achievement_type: 'missions', condition_value: 50, xp_reward: 500, is_legendary: false },
        { id: 13, name: 'El camino del guerrero', description: 'Completar las 7 misiones jefe', achievement_type: 'legendary', condition_value: 7, xp_reward: 3000, is_legendary: true },
        { id: 14, name: 'Sin caer', description: '60 días consecutivos sin bajar de nivel', achievement_type: 'legendary', condition_value: 60, xp_reward: 1000, is_legendary: true },
      ])

      // Determina cuáles están desbloqueados según el perfil actual
      const unlockedIds = []
      const w = prof.data.weight_current
      const s = prof.data.streak_days
      const active = prof.data.active_days_total

      if (w <= 104) unlockedIds.push(1)
      if (w <= 100) unlockedIds.push(2)
      if (w <= 95) unlockedIds.push(3)
      if (w <= 90) unlockedIds.push(4)
      if (w <= 85) unlockedIds.push(5)
      if (s >= 7) unlockedIds.push(6)
      if (s >= 30) unlockedIds.push(7)
      if (active >= 100) unlockedIds.push(8)
      if (active >= 150) unlockedIds.push(9)

      setUnlocked(unlockedIds)
    } catch {
      // silencioso por ahora
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <div className="ach-loading">Cargando...</div>

  const unlockedCount = unlocked.length
  const totalCount = achievements.length

  const grouped = {
    weight: achievements.filter(a => a.achievement_type === 'weight'),
    streak: achievements.filter(a => a.achievement_type === 'streak'),
    missions: achievements.filter(a => a.achievement_type === 'missions'),
    legendary: achievements.filter(a => a.achievement_type === 'legendary'),
  }

  const groupLabels = {
    weight: '⚖️ Peso',
    streak: '🔥 Racha',
    missions: '📋 Misiones',
    legendary: '👑 Legendarios',
  }

  return (
    <div className="achievements">
      <div className="ach-header">
        <h1>Logros</h1>
        <div className="ach-count">{unlockedCount}/{totalCount}</div>
      </div>

      <div className="ach-progress-bar">
        <div
          className="ach-progress-fill"
          style={{ width: `${(unlockedCount / totalCount) * 100}%` }}
        />
      </div>

      {Object.entries(grouped).map(([type, items]) => (
        <div key={type} className="ach-group">
          <div className="ach-group-title">{groupLabels[type]}</div>
          {items.map(a => {
            const isUnlocked = unlocked.includes(a.id)
            return (
              <div
                key={a.id}
                className={`ach-card ${isUnlocked ? 'unlocked' : ''} ${a.is_legendary ? 'legendary' : ''}`}
              >
                <div className="ach-icon">
                  {isUnlocked ? ACHIEVEMENT_ICONS[a.achievement_type] : '🔒'}
                </div>
                <div className="ach-info">
                  <div className="ach-name">{a.name}</div>
                  <div className="ach-desc">{a.description}</div>
                  <div className="ach-xp">+{a.xp_reward} XP</div>
                </div>
                {isUnlocked && <div className="ach-check">✓</div>}
              </div>
            )
          })}
        </div>
      ))}
    </div>
  )
}