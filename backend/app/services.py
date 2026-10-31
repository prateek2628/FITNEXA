from .config import settings
EXERCISES = {
 "none":{"push":["Incline push-ups","Knee or standard push-ups","Plank"],"legs":["Bodyweight squats","Reverse lunges","Glute bridges"],"full":["March in place","Bodyweight squats","Incline push-ups","Bird dogs"]},
 "dumbbells":{"push":["Dumbbell floor press","Dumbbell shoulder press","Overhead triceps extension"],"legs":["Goblet squats","Dumbbell Romanian deadlift","Reverse lunges"],"full":["Goblet squats","Dumbbell rows","Dumbbell floor press","Farmer carry"]},
 "full_gym":{"push":["Bench press","Seated shoulder press","Cable triceps press-down"],"legs":["Leg press","Romanian deadlift","Leg curl"],"full":["Leg press","Lat pulldown","Chest press","Cable row"]}}
def build_workout_plan(goal, level, days_per_week, session_minutes, equipment):
    split = (["full","legs","full","push","full","legs","full"] if goal=="fat_loss" else ["push","legs","full","push","legs","full","push"] if goal=="muscle_gain" else ["full","full","legs","full","full","legs","full"] if goal=="endurance" else ["full","legs","push","full","legs","push","full"])
    days=[]
    for i in range(days_per_week):
        focus=split[i]; exercises=EXERCISES[equipment][focus]
        days.append({"day":i+1,"focus":focus.title(),"duration_minutes":session_minutes,"warmup_minutes":5,"exercises":[{"name":n,"sets":2 if level=="beginner" else 3,"reps":"8-12" if "carry" not in n.lower() else "30-45 sec","rest_seconds":60 if level=="beginner" else 90} for n in exercises]})
    return {"goal":goal,"level":level,"days_per_week":days_per_week,"session_minutes":session_minutes,"equipment":equipment,"disclaimer":"General educational plan only. Adapt to your ability and stop if you feel pain. Seek qualified advice for injuries or medical conditions.","days":days}
def estimate_nutrition(data):
    multiplier={"low":1.2,"moderate":1.45,"high":1.65}[data.activity_level]
    base=10*data.weight_kg+6.25*data.height_cm-5*data.age
    maintenance=base*multiplier
    factor=0.85 if data.goal=="fat_loss" else 1.08 if data.goal=="muscle_gain" else 1.0
    calories=round(maintenance*factor/50)*50
    return {"estimated_daily_calories":calories,"range":[max(1200,calories-200),calories+200],"goal":data.goal,"note":"Rough educational estimate, not medical advice. Actual needs vary; avoid aggressive restriction and consult a registered dietitian for personalized guidance."}

async def ai_coach_reply(goal: str, message: str):
    try:
        from openai import AsyncOpenAI

        client = AsyncOpenAI(
            api_key=settings.openai_api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            max_retries=3,
            timeout=30.0,
)
        response = await client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are FitNexa, a cautious general fitness education assistant. "
                        "Give practical, non-diagnostic advice. Never diagnose, prescribe "
                        "treatment, promise results, or encourage extreme diets. For injury "
                        "or medical concerns, recommend a qualified professional. Keep replies concise."
                    )
                },
                {
                    "role": "user",
                    "content": f"User goal: {goal}. Message: {message}"
                }
            ],
            temperature=0.4
        )

        return {
            "reply": response.choices[0].message.content or "I couldn't generate a reply.",
            "mode": "ai"
        }

    except Exception as e:
        print(f"FitNexa AI error: {e}")
        return {
            "reply": "The AI provider is temporarily unavailable. Check your API key, model name, usage limits, and network connection, then try again.",
            "mode": "fallback"
        }
