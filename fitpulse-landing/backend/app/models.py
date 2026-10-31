from datetime import datetime
from sqlalchemy import Column, DateTime, Float, Integer, String, Text
from .database import Base
class UserProfile(Base):
    __tablename__ = "user_profiles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    height_cm = Column(Float, nullable=False)
    weight_kg = Column(Float, nullable=False)
    goal = Column(String(40), nullable=False)
    activity_level = Column(String(30), nullable=False, default="moderate")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
class WorkoutPlan(Base):
    __tablename__ = "workout_plans"
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, nullable=True)
    goal = Column(String(40), nullable=False)
    level = Column(String(30), nullable=False)
    days_per_week = Column(Integer, nullable=False)
    plan_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
