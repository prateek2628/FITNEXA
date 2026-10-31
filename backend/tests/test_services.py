from app.services import build_workout_plan, estimate_nutrition
from app.schemas import NutritionRequest
def test_workout_plan_has_requested_days():
    plan=build_workout_plan("general_fitness","beginner",4,30,"none")
    assert len(plan["days"])==4 and plan["days_per_week"]==4
def test_nutrition_estimate_returns_range():
    data=NutritionRequest(age=25,height_cm=170,weight_kg=70,activity_level="moderate",goal="general_fitness")
    result=estimate_nutrition(data)
    assert result["range"][0] < result["estimated_daily_calories"] < result["range"][1]
