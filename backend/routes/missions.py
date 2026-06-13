from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from datetime import date, timedelta
import random
from routes.user import check_and_grant_achievements

router = APIRouter(prefix="/missions", tags=["Misiones"])


def get_week_start(d: date) -> date:
    """Regresa el lunes de la semana de la fecha dada."""
    return d - timedelta(days=d.weekday())


def add_xp_to_user(user: models.User, xp: int, db: Session):
    """Suma XP al usuario y sube de nivel si corresponde."""
    user.xp_current += xp
    user.xp_total += xp

    while True:
        xp_needed = int(500 * user.level * (1.15 ** (user.level - 1)))
        if user.xp_current >= xp_needed and user.level < 100:
            user.xp_current -= xp_needed
            user.level += 1
        else:
            break

    db.commit()


def update_streak(user: models.User, db: Session):
    """Actualiza la racha del usuario."""
    today = date.today()
    yesterday = today - timedelta(days=1)

    # Verifica si ya contamos hoy (si hay más de 1 misión completada hoy, ya se contó)
    already_counted_today = db.query(models.DailyMission).filter(
        models.DailyMission.user_id == user.id,
        models.DailyMission.completed_date == today,
        models.DailyMission.completed == True
    ).count()

    if already_counted_today > 1:
        return

    # Verifica si hubo actividad ayer
    activity_yesterday = db.query(models.DailyMission).filter(
        models.DailyMission.user_id == user.id,
        models.DailyMission.completed_date == yesterday,
        models.DailyMission.completed == True
    ).count()

    if activity_yesterday > 0:
        user.streak_days += 1
    else:
        user.streak_days = 1

    user.active_days_total += 1
    db.commit()


@router.get("/daily")
def get_daily_missions(db: Session = Depends(get_db)):
    """Devuelve las misiones del día con su estado de completado."""
    user = db.query(models.User).filter(models.User.id == 1).first()
    today = date.today()

    applicable_missions = db.query(models.Mission).filter(
        models.Mission.is_active == True,
        models.Mission.mission_type.in_(["daily_nutrition", "daily_exercise"]),
        models.Mission.evolution_state_required == user.evolution_state
    ).all()

    nutrition_missions = db.query(models.Mission).filter(
        models.Mission.is_active == True,
        models.Mission.mission_type == "daily_nutrition"
    ).all()

    all_missions = nutrition_missions + [
        m for m in applicable_missions if m.mission_type == "daily_exercise"
    ]

    result = []
    for mission in all_missions:
        daily = db.query(models.DailyMission).filter(
            models.DailyMission.user_id == 1,
            models.DailyMission.mission_id == mission.id,
            models.DailyMission.completed_date == today
        ).first()

        result.append({
            "mission_id": mission.id,
            "name": mission.name,
            "description": mission.description,
            "mission_type": mission.mission_type,
            "xp_reward": mission.xp_reward,
            "coins_reward": mission.coins_reward,
            "completed": daily.completed if daily else False,
        })

    return {"date": str(today), "missions": result}


@router.post("/daily/{mission_id}/complete")
def complete_daily_mission(mission_id: int, db: Session = Depends(get_db)):
    """Marca una misión diaria como completada."""
    user = db.query(models.User).filter(models.User.id == 1).first()
    mission = db.query(models.Mission).filter(models.Mission.id == mission_id).first()
    today = date.today()

    if not mission:
        raise HTTPException(status_code=404, detail="Misión no encontrada")

    existing = db.query(models.DailyMission).filter(
        models.DailyMission.user_id == 1,
        models.DailyMission.mission_id == mission_id,
        models.DailyMission.completed_date == today
    ).first()

    if existing and existing.completed:
        raise HTTPException(status_code=400, detail="Misión ya completada hoy")

    multiplier = 1.0
    if user.streak_days >= 30:
        multiplier = 1.5
    elif user.streak_days >= 7:
        multiplier = 1.25
    elif user.streak_days >= 3:
        multiplier = 1.1

    xp_earned = int(mission.xp_reward * multiplier)
    coins_earned = mission.coins_reward

    if existing:
        existing.completed = True
        existing.xp_earned = xp_earned
        existing.coins_earned = coins_earned
    else:
        daily = models.DailyMission(
            user_id=1,
            mission_id=mission_id,
            completed_date=today,
            completed=True,
            xp_earned=xp_earned,
            coins_earned=coins_earned
        )
        db.add(daily)

    user.coins += coins_earned
    add_xp_to_user(user, xp_earned, db)
    update_streak(user, db)

    all_today = db.query(models.DailyMission).filter(
        models.DailyMission.user_id == 1,
        models.DailyMission.completed_date == today,
        models.DailyMission.completed == True
    ).count()

    nutrition_count = db.query(models.Mission).filter(
        models.Mission.mission_type == "daily_nutrition",
        models.Mission.is_active == True
    ).count()
    exercise_count = db.query(models.Mission).filter(
        models.Mission.mission_type == "daily_exercise",
        models.Mission.is_active == True,
        models.Mission.evolution_state_required == user.evolution_state
    ).count()
    total_missions = nutrition_count + exercise_count

    perfect_day = all_today >= total_missions
    if perfect_day:
        add_xp_to_user(user, 50, db)
        user.coins += 20
        db.commit()

        # Otorga logro de día perfecto
        perfect_achievement = db.query(models.Achievement).filter(
            models.Achievement.achievement_type == "missions",
            models.Achievement.condition_value == 1
        ).first()

        if perfect_achievement:
            already = db.query(models.UserAchievement).filter(
                models.UserAchievement.user_id == user.id,
                models.UserAchievement.achievement_id == perfect_achievement.id
            ).first()
            if not already:
                db.add(models.UserAchievement(
                    user_id=user.id,
                    achievement_id=perfect_achievement.id,
                    unlocked_date=date.today()
                ))
                user.xp_current += perfect_achievement.xp_reward
                user.xp_total += perfect_achievement.xp_reward
                db.commit()

    return {
        "message": "Misión completada",
        "xp_earned": xp_earned,
        "coins_earned": coins_earned,
        "multiplier": multiplier,
        "perfect_day": perfect_day,
        "user_level": user.level,
        "user_xp": user.xp_current,
        "user_coins": user.coins,
    }


@router.get("/weekly/knowledge")
def get_weekly_knowledge(db: Session = Depends(get_db)):
    """Devuelve las 4 actividades de conocimiento asignadas esta semana."""
    today = date.today()
    week_start = get_week_start(today)

    assignments = db.query(models.WeeklyKnowledge).filter(
        models.WeeklyKnowledge.user_id == 1,
        models.WeeklyKnowledge.week_start == week_start
    ).all()

    if not assignments:
        categories = ["Arte", "Bienestar", "Ciencia", "Espiritualidad", "Gastronomia", "Historia", "Musica"]
        selected_categories = random.sample(categories, 4)

        for category in selected_categories:
            activities = db.query(models.KnowledgeActivity).filter(
                models.KnowledgeActivity.category == category,
                models.KnowledgeActivity.is_active == True
            ).all()

            if activities:
                activity = random.choice(activities)
                assignment = models.WeeklyKnowledge(
                    user_id=1,
                    activity_id=activity.id,
                    week_start=week_start,
                    completed=False
                )
                db.add(assignment)

        db.commit()

        assignments = db.query(models.WeeklyKnowledge).filter(
            models.WeeklyKnowledge.user_id == 1,
            models.WeeklyKnowledge.week_start == week_start
        ).all()

    result = []
    for a in assignments:
        result.append({
            "assignment_id": a.id,
            "activity_id": a.activity_id,
            "name": a.activity.name,
            "category": a.activity.category,
            "xp_reward": a.activity.xp_reward,
            "completed": a.completed,
            "completed_date": str(a.completed_date) if a.completed_date else None,
        })

    return {"week_start": str(week_start), "activities": result}


@router.post("/weekly/knowledge/{assignment_id}/complete")
def complete_knowledge_mission(assignment_id: int, db: Session = Depends(get_db)):
    """Marca una actividad de conocimiento como completada."""
    user = db.query(models.User).filter(models.User.id == 1).first()
    assignment = db.query(models.WeeklyKnowledge).filter(
        models.WeeklyKnowledge.id == assignment_id,
        models.WeeklyKnowledge.user_id == 1
    ).first()

    if not assignment:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")

    if assignment.completed:
        raise HTTPException(status_code=400, detail="Actividad ya completada")

    today = date.today()
    week_start = get_week_start(today)

    if assignment.week_start != week_start:
        raise HTTPException(status_code=400, detail="Esta actividad es de una semana anterior")

    completed_today = db.query(models.WeeklyKnowledge).filter(
        models.WeeklyKnowledge.user_id == 1,
        models.WeeklyKnowledge.completed_date == today,
        models.WeeklyKnowledge.completed == True
    ).count()

    if completed_today >= 2:
        raise HTTPException(status_code=400, detail="Máximo 2 actividades de conocimiento por día")

    xp_earned = assignment.activity.xp_reward
    assignment.completed = True
    assignment.completed_date = today

    user.coins += 5
    add_xp_to_user(user, xp_earned, db)

    return {
        "message": "Actividad completada",
        "activity": assignment.activity.name,
        "xp_earned": xp_earned,
        "user_level": user.level,
        "user_xp": user.xp_current,
    }


@router.post("/weekly/knowledge/refresh")
def refresh_knowledge_missions(db: Session = Depends(get_db)):
    """Refresca las actividades de conocimiento de la semana (cuesta 50 monedas)."""
    user = db.query(models.User).filter(models.User.id == 1).first()
    today = date.today()
    week_start = get_week_start(today)

    if user.coins < 50:
        raise HTTPException(status_code=400, detail="No tienes suficientes monedas (necesitas 50)")

    already_refreshed = db.query(models.WeeklyKnowledge).filter(
        models.WeeklyKnowledge.user_id == 1,
        models.WeeklyKnowledge.week_start == week_start,
        models.WeeklyKnowledge.refreshed == True
    ).first()

    if already_refreshed:
        raise HTTPException(status_code=400, detail="Ya usaste el refresh esta semana")

    db.query(models.WeeklyKnowledge).filter(
        models.WeeklyKnowledge.user_id == 1,
        models.WeeklyKnowledge.week_start == week_start,
        models.WeeklyKnowledge.completed == False
    ).delete()

    user.coins -= 50

    categories = ["Arte", "Bienestar", "Ciencia", "Espiritualidad", "Gastronomia", "Historia", "Musica"]
    selected_categories = random.sample(categories, 4)

    for category in selected_categories:
        activities = db.query(models.KnowledgeActivity).filter(
            models.KnowledgeActivity.category == category,
            models.KnowledgeActivity.is_active == True
        ).all()

        if activities:
            activity = random.choice(activities)
            assignment = models.WeeklyKnowledge(
                user_id=1,
                activity_id=activity.id,
                week_start=week_start,
                completed=False,
                refreshed=True
            )
            db.add(assignment)

    db.commit()

    return {"message": "Actividades refrescadas", "coins_remaining": user.coins}