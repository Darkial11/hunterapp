import { useEffect, useState } from 'react'
import api from '../utils/api'
import './Rewards.css'

export default function Rewards() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [claiming, setClaiming] = useState(null)
  const [toast, setToast] = useState(null)
  const [tab, setTab] = useState('weekly')

  useEffect(() => {
    fetchRewards()
  }, [])

  async function fetchRewards() {
    try {
      const res = await api.get('/rewards/')
      setData(res.data)
    } finally {
      setLoading(false)
    }
  }

  function showToast(message, type = 'success') {
    setToast({ message, type })
    setTimeout(() => setToast(null), 3000)
  }

  async function claimReward(rewardId, rewardName) {
    const confirmed = window.confirm(`¿Reclamar recompensa?\n\n"${rewardName}"`)
    if (!confirmed) return

    setClaiming(rewardId)
    try {
      await api.post(`/rewards/${rewardId}/claim`)
      showToast(`Recompensa reclamada: ${rewardName} 🎉`)
      fetchRewards()
    } catch (err) {
      showToast(err.response?.data?.detail || 'Error al reclamar', 'error')
    } finally {
      setClaiming(null)
    }
  }

  if (loading) return <div className="rewards-loading">Cargando...</div>

  const weekly = data.rewards.filter(r => r.reward_type === 'weekly')
  const milestones = data.rewards.filter(r => r.reward_type === 'milestone')

  return (
    <div className="rewards">
      {toast && <div className={`toast ${toast.type}`}>{toast.message}</div>}

      <div className="rewards-header">
        <h1>Recompensas</h1>
        <div className="rewards-coins">🪙 {data.user_coins}</div>
      </div>

      <div className="rewards-week-info">
        Misiones completadas esta semana: <strong>{data.weekly_completion}%</strong>
      </div>

      <div className="tabs">
        <button
          className={`tab ${tab === 'weekly' ? 'active' : ''}`}
          onClick={() => setTab('weekly')}
        >
          Semanales
        </button>
        <button
          className={`tab ${tab === 'milestone' ? 'active' : ''}`}
          onClick={() => setTab('milestone')}
        >
          Hitos
        </button>
      </div>

      {tab === 'weekly' && (
        <div className="rewards-list">
          {weekly.map(r => (
            <RewardCard
              key={r.id}
              reward={r}
              onClaim={() => claimReward(r.id, r.name)}
              claiming={claiming === r.id}
            />
          ))}
        </div>
      )}

      {tab === 'milestone' && (
        <div className="rewards-list">
          {milestones.map(r => (
            <RewardCard
              key={r.id}
              reward={r}
              onClaim={() => claimReward(r.id, r.name)}
              claiming={claiming === r.id}
            />
          ))}
        </div>
      )}
    </div>
  )
}

function RewardCard({ reward, onClaim, claiming }) {
  return (
    <div className={`reward-card ${reward.available ? 'available' : 'locked'}`}>
      <div className="reward-info">
        <div className="reward-name">{reward.name}</div>
        <div className="reward-condition">{reward.condition_description}</div>
        {reward.coin_cost > 0 && (
          <div className="reward-cost">🪙 {reward.coin_cost} monedas</div>
        )}
        {!reward.available && reward.reason && (
          <div className="reward-reason">{reward.reason}</div>
        )}
      </div>
      <button
        className={`claim-btn ${reward.available ? 'active' : 'disabled'}`}
        onClick={onClaim}
        disabled={!reward.available || claiming}
      >
        {claiming ? '...' : reward.available ? '✓' : '🔒'}
      </button>
    </div>
  )
}