from typing import Literal
from pydantic import BaseModel, Field
Goal = Literal["fat_loss", "muscle_gain", "general_fitness", "endurance"]
Level = Literal["beginner", "intermediate", "advanced"]
class ProfileCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=16, le=100)
    height_cm: float = Field(gt=80, le=250)
    weight_kg: float = Field(gt=25, le=350)
    goal: Goal
    activity_level: Literal["low", "moderate", "high"] = "moderate"
class ProfileOut(ProfileCreate):
    id: int
    model_config = {"from_attributes": True}
class WorkoutRequest(BaseModel):
    goal: Goal
    level: Level = "beginner"
    days_per_week: int = Field(default=3, ge=1, le=7)
    session_minutes: int = Field(default=45, ge=15, le=120)
    equipment: Literal["none", "dumbbells", "full_gym"] = "none"
class NutritionRequest(BaseModel):
    age: int = Field(ge=16, le=100)
    height_cm: float = Field(gt=80, le=250)
    weight_kg: float = Field(gt=25, le=350)
    activity_level: Literal["low", "moderate", "high"] = "moderate"
    goal: Goal
class CoachRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    goal: Goal = "general_fitness"
