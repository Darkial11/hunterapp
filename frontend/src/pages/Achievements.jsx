import { useEffect, useState } from 'react'
import api from '../utils/api'
import './Achievements.css'

const ACHIEVEMENT_ICONS = {
  weight: '⚖️',
  streak: '🔥',
  missions: '📋',
  legendary: '👑',
}

const GROUP_LABELS = {
  weight: '⚖️ Peso',
  streak: '🔥 Racha',
  missions: '📋 Misiones',
  legendary: '👑 Legendarios',
}

export default function Achievements() {
  const [achievements, setAchievements] = useState([])
  const [unlockedIds, setUnlockedIds] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchData()
  }, [])

  async function fetchData() {
    try {
      const [achRes, unlockedRes] = await Promise.all([
        api.get('/user/achievements'),
        api.get('/user/achievements/unlocked'),
      ])
      setAchievements(achRes.data)
      setUnlockedIds(unlockedRes.data.map(u => u.achievement_id))
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <div className="ach-loading">Cargando...</div>

  const unlockedCount = unlockedIds.length
  const totalCount = achievements.length

  const grouped = {
    weight: achievements.filter(a => a.achievement_type === 'weight'),
    streak: achievements.filter(a => a.achievement_type === 'streak'),
    missions: achievements.filter(a => a.achievement_type === 'missions'),
    legendary: achievements.filter(a => a.achievement_type === 'legendary'),
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
          style={{ width: `${totalCount > 0 ? (unlockedCount / totalCount) * 100 : 0}%` }}
        />
      </div>

      {Object.entries(grouped).map(([type, items]) => (
        <div key={type} className="ach-group">
          <div className="ach-group-title">{GROUP_LABELS[type]}</div>
          {items.map(a => {
            const isUnlocked = unlockedIds.includes(a.id)
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