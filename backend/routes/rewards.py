from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from datetime import date, timedelta

router = APIRouter(prefix="/rewards", tags=["Recompensas"])


def get_week_start(d: date) -> date:
    return d - timedelta(days=d.weekday())


def get_weekly_completion(user_id: int, week_start: date, db: Session) -> float:
    """Calcula el % de misiones completadas en la semana."""
    week_end = week_start + timedelta(days=6)
    
    completed = db.query(models.DailyMission).filter(
        models.DailyMission.user_id == user_id,
        models.DailyMission.completed == True,
        models.DailyMission.completed_date >= week_start,
        models.DailyMission.completed_date <= week_end
    ).count()

    # Máximo posible: 6 misiones/día × 7 días (aproximado)
    max_possible = 6 * 7
    return min(completed / max_possible, 1.0)


@router.get("/")
def get_rewards(db: Session = Depends(get_db)):
    """Devuelve todas las recompensas con su estado de disponibilidad."""
    user = db.query(models.User).filter(models.User.id == 1).first()
    today = date.today()
    week_start = get_week_start(today)
    weekly_completion = get_weekly_completion(1, week_start, db)

    rewards = db.query(models.Reward).filter(models.Reward.is_active == True).all()

    result = []
    for r in rewards:
        available = False
        reason = ""

        if r.reward_type == "weekly":
            if user.coins < r.coin_cost:
                reason = f"Necesitas {r.coin_cost} monedas (tienes {user.coins})"
            elif r.requires_perfect_week and weekly_completion < 1.0:
                reason = "Requiere semana perfecta (100% misiones)"
            elif r.requires_streak > 0 and user.streak_days < r.requires_streak:
                reason = f"Requiere racha de {r.requires_streak} días (tienes {user.streak_days})"
            elif weekly_completion < r.min_weekly_completion:
                reason = f"Requiere {int(r.min_weekly_completion * 100)}% de misiones completadas"
            else:
                available = True

        elif r.reward_type == "milestone":
            if r.milestone_kg and user.weight_current <= r.milestone_kg:
                available = True
            else:
                reason = f"Llega a {r.milestone_kg} kg para desbloquear"

        result.append({
            "id": r.id,
            "name": r.name,
            "reward_type": r.reward_type,
            "coin_cost": r.coin_cost,
            "condition_description": r.condition_description,
            "available": available,
            "reason": reason,
            "milestone_kg": r.milestone_kg,
        })

    return {
        "user_coins": user.coins,
        "weekly_completion": round(weekly_completion * 100, 1),
        "rewards": result
    }


@router.post("/{reward_id}/claim")
def claim_reward(reward_id: int, db: Session = Depends(get_db)):
    """Reclama una recompensa."""
    user = db.query(models.User).filter(models.User.id == 1).first()
    reward = db.query(models.Reward).filter(models.Reward.id == reward_id).first()
    today = date.today()
    week_start = get_week_start(today)

    if not reward:
        raise HTTPException(status_code=404, detail="Recompensa no encontrada")

    if user.coins < reward.coin_cost:
        raise HTTPException(status_code=400, detail=f"No tienes suficientes monedas. Necesitas {reward.coin_cost}, tienes {user.coins}")

    # Verifica que no haya reclamado una recompensa semanal esta semana
    if reward.reward_type == "weekly":
        already_claimed = db.query(models.ClaimedReward).filter(
            models.ClaimedReward.user_id == 1,
            models.ClaimedReward.week_start == week_start,
            models.ClaimedReward.reward_id == reward_id
        ).first()

        if already_claimed:
            raise HTTPException(status_code=400, detail="Ya reclamaste esta recompensa esta semana")

        weekly_completion = get_weekly_completion(1, week_start, db)

        if reward.requires_perfect_week and weekly_completion < 1.0:
            raise HTTPException(status_code=400, detail="Requiere semana perfecta")
        if reward.requires_streak > 0 and user.streak_days < reward.requires_streak:
            raise HTTPException(status_code=400, detail=f"Requiere racha de {reward.requires_streak} días")
        if weekly_completion < reward.min_weekly_completion:
            raise HTTPException(status_code=400, detail="No cumples el % mínimo de misiones esta semana")

    elif reward.reward_type == "milestone":
        if reward.milestone_kg and user.weight_current > reward.milestone_kg:
            raise HTTPException(status_code=400, detail=f"Necesitas llegar a {reward.milestone_kg} kg primero")

        already_claimed = db.query(models.ClaimedReward).filter(
            models.ClaimedReward.user_id == 1,
            models.ClaimedReward.reward_id == reward_id
        ).first()

        if already_claimed:
            raise HTTPException(status_code=400, detail="Este hito ya fue reclamado")

    claimed = models.ClaimedReward(
        user_id=1,
        reward_id=reward_id,
        claimed_date=today,
        coins_spent=reward.coin_cost,
        week_start=week_start if reward.reward_type == "weekly" else None
    )
    db.add(claimed)
    user.coins -= reward.coin_cost
    db.commit()

    return {
        "message": f"Recompensa reclamada: {reward.name}",
        "coins_spent": reward.coin_cost,
        "coins_remaining": user.coins
    }


@router.get("/history")
def get_reward_history(db: Session = Depends(get_db)):
    """Historial de recompensas reclamadas."""
    history = db.query(models.ClaimedReward).filter(
        models.ClaimedReward.user_id == 1
    ).order_by(models.ClaimedReward.claimed_date.desc()).all()

    return [
        {
            "reward_name": h.reward.name,
            "claimed_date": str(h.claimed_date),
            "coins_spent": h.coins_spent,
        }
        for h in history
    ]