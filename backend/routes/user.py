from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from datetime import date

router = APIRouter(prefix="/user", tags=["Usuario"])


def xp_needed_for_level(level: int) -> int:
    """XP necesario para subir del nivel N al N+1."""
    return int(500 * level * (1.15 ** (level - 1)))


def get_evolution_state(level: int, weight: float, active_days: int) -> int:
    """Determina el estado de evolución según nivel, peso y días activos."""
    if active_days >= 150 and weight <= 85.0:
        return 7
    elif active_days >= 120 and weight <= 88.0:
        return 6
    elif active_days >= 90 and weight <= 91.0:
        return 5
    elif active_days >= 60 and weight <= 95.0:
        return 4
    elif active_days >= 30 and weight <= 99.0:
        return 3
    elif active_days >= 7 and weight <= 102.0:
        return 2
    elif level >= 1:
        return 1
    return 0

def check_and_grant_achievements(user: models.User, db: Session):
    """Verifica condiciones de logros y los otorga si se cumplen."""
    from datetime import date
    
    all_achievements = db.query(models.Achievement).all()
    
    for achievement in all_achievements:
        # Verifica si ya fue otorgado
        already_unlocked = db.query(models.UserAchievement).filter(
            models.UserAchievement.user_id == user.id,
            models.UserAchievement.achievement_id == achievement.id
        ).first()
        
        if already_unlocked:
            continue
        
        unlocked = False
        
        if achievement.achievement_type == "weight":
            if user.weight_current <= achievement.condition_value:
                unlocked = True
        
        elif achievement.achievement_type == "streak":
            if user.streak_days >= achievement.condition_value:
                unlocked = True
        
        elif achievement.achievement_type == "missions":
            if achievement.condition_value == 1:
                # Día perfecto — se maneja en missions.py
                pass
            else:
                completed_count = db.query(models.DailyMission).filter(
                    models.DailyMission.user_id == user.id,
                    models.DailyMission.completed == True
                ).count()
                if completed_count >= achievement.condition_value:
                    unlocked = True
        
        if unlocked:
            user_achievement = models.UserAchievement(
                user_id=user.id,
                achievement_id=achievement.id,
                unlocked_date=date.today()
            )
            db.add(user_achievement)
            user.xp_current += achievement.xp_reward
            user.xp_total += achievement.xp_reward
    
    db.commit()

@router.get("/profile")
def get_profile(db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == 1).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    xp_needed = xp_needed_for_level(user.level)
    evolution_state = get_evolution_state(
        user.level, user.weight_current, user.active_days_total
    )

    # Actualiza estado de evolución si cambió
    if evolution_state != user.evolution_state:
        user.evolution_state = evolution_state
        db.commit()

    return {
        "id": user.id,
        "name": user.name,
        "level": user.level,
        "xp_current": user.xp_current,
        "xp_needed": xp_needed,
        "xp_total": user.xp_total,
        "coins": user.coins,
        "streak_days": user.streak_days,
        "active_days_total": user.active_days_total,
        "evolution_state": user.evolution_state,
        "weight_initial": user.weight_initial,
        "weight_current": user.weight_current,
        "weight_goal": user.weight_goal,
        "height_cm": user.height_cm,
        "shield_available": user.shield_available,
        "fault_points_week": user.fault_points_week,
    }


@router.post("/weight")
def log_weight(weight_kg: float, db: Session = Depends(get_db)):
    """Registra el peso del día."""
    if weight_kg < 40 or weight_kg > 200:
        raise HTTPException(status_code=400, detail="Peso fuera de rango válido")

    user = db.query(models.User).filter(models.User.id == 1).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    today = date.today()

    # Verifica si ya registró peso hoy
    existing = db.query(models.WeightLog).filter(
        models.WeightLog.user_id == 1,
        models.WeightLog.logged_date == today
    ).first()

    if existing:
        existing.weight_kg = weight_kg
    else:
        log = models.WeightLog(user_id=1, weight_kg=weight_kg, logged_date=today)
        db.add(log)

    user.weight_current = weight_kg
    db.commit()

    check_and_grant_achievements(user, db)

    return {"message": "Peso registrado", "weight_kg": weight_kg, "date": str(today)}


@router.get("/weight/history")
def get_weight_history(db: Session = Depends(get_db)):
    """Devuelve el historial de peso ordenado por fecha."""
    logs = db.query(models.WeightLog).filter(
        models.WeightLog.user_id == 1
    ).order_by(models.WeightLog.logged_date.asc()).all()

    return [
        {"date": str(log.logged_date), "weight_kg": log.weight_kg}
        for log in logs
    ]

@router.put("/profile")
def update_profile(
    weight_initial: float = None,
    weight_current: float = None,
    weight_goal: float = None,
    height_cm: int = None,
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == 1).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if weight_current and (weight_current < 40 or weight_current > 200):
        raise HTTPException(status_code=400, detail="Peso fuera de rango válido")
    if weight_goal and (weight_goal < 40 or weight_goal > 200):
        raise HTTPException(status_code=400, detail="Peso meta fuera de rango válido")
    if height_cm and (height_cm < 100 or height_cm > 250):
        raise HTTPException(status_code=400, detail="Estatura fuera de rango válido")

    if weight_initial is not None:
        user.weight_initial = weight_initial
    if weight_current is not None:
        user.weight_current = weight_current
    if weight_goal is not None:
        user.weight_goal = weight_goal
    if height_cm is not None:
        user.height_cm = height_cm

    db.commit()
    return {"message": "Perfil actualizado correctamente"}

@router.get("/achievements")
def get_achievements(db: Session = Depends(get_db)):
    """Devuelve el catálogo completo de logros."""
    achievements = db.query(models.Achievement).all()
    return [
        {
            "id": a.id,
            "name": a.name,
            "description": a.description,
            "achievement_type": a.achievement_type,
            "condition_value": a.condition_value,
            "xp_reward": a.xp_reward,
            "is_legendary": a.is_legendary,
        }
        for a in achievements
    ]


@router.get("/achievements/unlocked")
def get_unlocked_achievements(db: Session = Depends(get_db)):
    """Devuelve los logros desbloqueados por el usuario."""
    unlocked = db.query(models.UserAchievement).filter(
        models.UserAchievement.user_id == 1
    ).all()
    return [
        {
            "achievement_id": u.achievement_id,
            "unlocked_date": str(u.unlocked_date),
        }
        for u in unlocked
    ]
