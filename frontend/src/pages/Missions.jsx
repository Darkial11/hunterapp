import { useEffect, useState } from 'react'
import api from '../utils/api'
import './Missions.css'

const [refreshing, setRefreshing] = useState(false)

const CATEGORY_COLORS = {
  Arte: '#ff6b9d',
  Bienestar: '#51cf66',
  Ciencia: '#74c0fc',
  Espiritualidad: '#cc5de8',
  Gastronomia: '#ffa94d',
  Historia: '#f59f00',
  Musica: '#20c997',
}

export default function Missions() {
  const [tab, setTab] = useState('daily')
  const [dailyMissions, setDailyMissions] = useState([])
  const [weeklyKnowledge, setWeeklyKnowledge] = useState([])
  const [loading, setLoading] = useState(true)
  const [completing, setCompleting] = useState(null)
  const [toast, setToast] = useState(null)

  useEffect(() => {
    fetchAll()
  }, [])

  async function refreshKnowledge() {
    const confirmed = window.confirm('¿Actualizar actividades de conocimiento? Cuesta 50 🪙 y solo puedes hacerlo una vez por semana.')
    if (!confirmed) return

    setRefreshing(true)
    try {
      await api.post('/missions/weekly/knowledge/refresh')
      showToast('Actividades actualizadas ✓')
      fetchAll()
    } catch (err) {
      showToast(err.response?.data?.detail || 'Error al actualizar', 'error')
    } finally {
      setRefreshing(false)
    }
  }

  async function fetchAll() {
    setLoading(true)
    try {
      const [daily, knowledge] = await Promise.all([
        api.get('/missions/daily'),
        api.get('/missions/weekly/knowledge'),
      ])
      setDailyMissions(daily.data.missions)
      setWeeklyKnowledge(knowledge.data.activities)
    } catch {
      showToast('Error al cargar misiones', 'error')
    } finally {
      setLoading(false)
    }
  }

  function showToast(message, type = 'success') {
    setToast({ message, type })
    setTimeout(() => setToast(null), 3000)
  }

async function completeDaily(missionId, missionName) {
  const confirmed = window.confirm(`¿Completaste la misión?\n\n"${missionName}"`)
  if (!confirmed) return

  setCompleting(missionId)
  try {
    const res = await api.post(`/missions/daily/${missionId}/complete`)
    const data = res.data
    showToast(`+${data.xp_earned} XP ${data.perfect_day ? '🎉 ¡Día perfecto! +50 XP bonus' : ''}`)
    fetchAll()
  } catch (err) {
    showToast(err.response?.data?.detail || 'Error al completar misión', 'error')
  } finally {
    setCompleting(null)
  }
}

async function completeKnowledge(assignmentId, activityName) {
  const confirmed = window.confirm(`¿Completaste esta actividad?\n\n"${activityName}"`)
  if (!confirmed) return

  setCompleting(assignmentId)
  try {
    const res = await api.post(`/missions/weekly/knowledge/${assignmentId}/complete`)
    showToast(`+${res.data.xp_earned} XP — ${res.data.activity}`)
    fetchAll()
  } catch (err) {
    showToast(err.response?.data?.detail || 'Error al completar actividad', 'error')
  } finally {
    setCompleting(null)
  }
}

  const nutritionMissions = dailyMissions.filter(m => m.mission_type === 'daily_nutrition')
  const exerciseMissions = dailyMissions.filter(m => m.mission_type === 'daily_exercise')
  const completedCount = dailyMissions.filter(m => m.completed).length
  const totalCount = dailyMissions.length
  const progressPercent = totalCount > 0 ? (completedCount / totalCount) * 100 : 0

  return (
    <div className="missions">
      {toast && (
        <div className={`toast ${toast.type}`}>{toast.message}</div>
      )}

      <div className="missions-header">
        <h1>Misiones</h1>
        <div className="missions-progress-text">{completedCount}/{totalCount} completadas</div>
      </div>

      <div className="missions-progress-bar">
        <div className="missions-progress-fill" style={{ width: `${progressPercent}%` }} />
      </div>

      {/* Tabs */}
      <div className="tabs">
        <button
          className={`tab ${tab === 'daily' ? 'active' : ''}`}
          onClick={() => setTab('daily')}
        >
          Diarias
        </button>
        <button
          className={`tab ${tab === 'knowledge' ? 'active' : ''}`}
          onClick={() => setTab('knowledge')}
        >
          Conocimiento
        </button>
      </div>

      {loading ? (
        <div className="missions-loading">Cargando...</div>
      ) : (
        <>
          {tab === 'daily' && (
            <div className="missions-list">
              <div className="mission-group-title">💪 Ejercicio</div>
              {exerciseMissions.map(m => (
                <MissionCard
                  key={m.mission_id}
                  mission={m}                  
                  onComplete={() => completeDaily(m.mission_id, m.name)}
                  completing={completing === m.mission_id}
                />
              ))}

              <div className="mission-group-title">🥗 Nutrición</div>
              {nutritionMissions.map(m => (
                <MissionCard
                  key={m.mission_id}
                  mission={m}
                  onComplete={() => completeDaily(m.mission_id, m.name)}
                  completing={completing === m.mission_id}
                />
              ))}
            </div>
          )}

          {tab === 'knowledge' && (
            <div className="missions-list">
              <div className="knowledge-header">
                <div className="knowledge-subtitle">
                  4 actividades aleatorias esta semana
                </div>
                <button
                  className="refresh-btn"
                  onClick={refreshKnowledge}
                  disabled={refreshing}
                >
                  {refreshing ? '...' : '🔄 Actualizar — 50 🪙'}
                </button>
              </div>
              {weeklyKnowledge.map(a => (
                <KnowledgeCard
                  key={a.assignment_id}
                  activity={a}
                  onComplete={() => completeKnowledge(a.assignment_id, a.name)}
                  completing={completing === a.assignment_id}
                />
              ))}
            </div>
          )}
        </>
      )}
    </div>
  )
}

function MissionCard({ mission, onComplete, completing }) {
  return (
    <div className={`mission-card ${mission.completed ? 'completed' : ''}`}>
      <div className="mission-info">
        <div className="mission-name">{mission.name}</div>
        <div className="mission-desc">{mission.description}</div>
        <div className="mission-rewards">
          <span className="xp-badge">+{mission.xp_reward} XP</span>
          <span className="coin-badge">🪙 {mission.coins_reward}</span>
        </div>
      </div>
      <button
        className={`complete-btn ${mission.completed ? 'done' : ''}`}
        onClick={onComplete}
        disabled={mission.completed || completing}
      >
        {mission.completed ? '✓' : completing ? '...' : '○'}
      </button>
    </div>
  )
}

function KnowledgeCard({ activity, onComplete, completing }) {
  const color = CATEGORY_COLORS[activity.category] || '#4a9eff'
  return (
    <div className={`mission-card ${activity.completed ? 'completed' : ''}`}>
      <div className="mission-info">
        <div className="category-tag" style={{ color, borderColor: color }}>
          {activity.category}
        </div>
        <div className="mission-name">{activity.name}</div>
        <div className="mission-rewards">
          <span className="xp-badge">+{activity.xp_reward} XP</span>
        </div>
      </div>
      <button
        className={`complete-btn ${activity.completed ? 'done' : ''}`}
        onClick={onComplete}
        disabled={activity.completed || completing}
      >
        {activity.completed ? '✓' : completing ? '...' : '○'}
      </button>
    </div>
  )
}