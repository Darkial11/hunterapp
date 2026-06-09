from sqlalchemy import (
    Column, Integer, String, Float, Boolean,
    DateTime, ForeignKey, Text, Date
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default="Darkial")
    weight_current = Column(Float, default=105.0)   # kg actuales
    weight_initial = Column(Float, default=105.0)
    weight_goal = Column(Float, default=85.0)        # kg meta
    height_cm = Column(Integer, default=182)
    level = Column(Integer, default=1)
    xp_current = Column(Integer, default=0)          # XP dentro del nivel actual
    xp_total = Column(Integer, default=0)            # XP acumulado histórico
    coins = Column(Integer, default=0)
    streak_days = Column(Integer, default=0)         # racha actual en días
    active_days_total = Column(Integer, default=0)   # días activos acumulados
    evolution_state = Column(Integer, default=0)     # 0 al 7
    shield_available = Column(Boolean, default=True) # escudo mensual
    shield_used_this_month = Column(Boolean, default=False)
    fault_points_week = Column(Integer, default=0)   # puntos de falla semana actual
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    weight_logs = relationship("WeightLog", back_populates="user")
    daily_missions = relationship("DailyMission", back_populates="user")
    claimed_rewards = relationship("ClaimedReward", back_populates="user")
    achievements = relationship("UserAchievement", back_populates="user")
    weekly_knowledge = relationship("WeeklyKnowledge", back_populates="user")
    penalties = relationship("Penalty", back_populates="user")


class WeightLog(Base):
    __tablename__ = "weight_log"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    weight_kg = Column(Float, nullable=False)
    logged_date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="weight_logs")


class Mission(Base):
    """Catálogo de misiones — no cambia en tiempo de ejecución."""
    __tablename__ = "missions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    mission_type = Column(String, nullable=False)  # daily_exercise, daily_nutrition, weekly_exercise, boss
    xp_reward = Column(Integer, nullable=False)
    coins_reward = Column(Integer, default=5)
    evolution_state_required = Column(Integer, default=0)  # desde qué estado aplica
    is_active = Column(Boolean, default=True)


class DailyMission(Base):
    """Registro de misiones completadas por día."""
    __tablename__ = "daily_missions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    mission_id = Column(Integer, ForeignKey("missions.id"))
    completed_date = Column(Date, nullable=False)
    completed = Column(Boolean, default=False)
    xp_earned = Column(Integer, default=0)
    coins_earned = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="daily_missions")
    mission = relationship("Mission")


class KnowledgeActivity(Base):
    """Catálogo de 180 actividades de conocimiento."""
    __tablename__ = "knowledge_activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)  # Arte, Bienestar, Ciencia, Espiritualidad, Gastronomia, Historia, Musica
    xp_reward = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)


class WeeklyKnowledge(Base):
    """4 actividades aleatorias asignadas cada lunes."""
    __tablename__ = "weekly_knowledge"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    activity_id = Column(Integer, ForeignKey("knowledge_activities.id"))
    week_start = Column(Date, nullable=False)   # lunes de esa semana
    completed = Column(Boolean, default=False)
    completed_date = Column(Date)
    refreshed = Column(Boolean, default=False)  # si fue parte de un refresh (cuesta 50 monedas)

    user = relationship("User", back_populates="weekly_knowledge")
    activity = relationship("KnowledgeActivity")


class Reward(Base):
    """Catálogo de recompensas semanales y de hito."""
    __tablename__ = "rewards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    reward_type = Column(String, nullable=False)  # weekly, milestone
    coin_cost = Column(Integer, default=0)
    condition_description = Column(Text)          # descripción de la condición
    min_weekly_completion = Column(Float, default=0.8)  # % mínimo de misiones
    requires_km = Column(Integer, default=0)      # km requeridos esa semana (cerveza=10)
    requires_streak = Column(Integer, default=0)  # días de racha requeridos
    requires_perfect_week = Column(Boolean, default=False)
    milestone_kg = Column(Float)                  # solo para hitos (100, 95, 90, 85)
    is_active = Column(Boolean, default=True)


class ClaimedReward(Base):
    """Recompensas reclamadas por el usuario."""
    __tablename__ = "claimed_rewards"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    reward_id = Column(Integer, ForeignKey("rewards.id"))
    claimed_date = Column(Date, nullable=False)
    coins_spent = Column(Integer, default=0)
    week_start = Column(Date)  # semana a la que pertenece (si es semanal)

    user = relationship("User", back_populates="claimed_rewards")
    reward = relationship("Reward")


class Penalty(Base):
    """Registro de penalizaciones aplicadas."""
    __tablename__ = "penalties"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    penalty_type = Column(String, nullable=False)
    xp_lost = Column(Integer, default=0)
    fault_points = Column(Integer, default=0)
    description = Column(Text)
    applied_date = Column(Date, nullable=False)
    cancelled_by_shield = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="penalties")


class Achievement(Base):
    """Catálogo de logros disponibles."""
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    achievement_type = Column(String)  # weight, streak, missions, legendary
    condition_value = Column(Float)    # el número que hay que alcanzar
    xp_reward = Column(Integer, default=0)
    is_legendary = Column(Boolean, default=False)


class UserAchievement(Base):
    """Logros desbloqueados por el usuario."""
    __tablename__ = "user_achievements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    achievement_id = Column(Integer, ForeignKey("achievements.id"))
    unlocked_date = Column(Date, nullable=False)

    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement")