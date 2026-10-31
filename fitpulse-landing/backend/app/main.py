import json
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .config import settings
from .database import Base, engine, get_db
from .models import UserProfile, WorkoutPlan
from .schemas import CoachRequest, NutritionRequest, ProfileCreate, ProfileOut, WorkoutRequest
from .services import ai_coach_reply, build_workout_plan, estimate_nutrition
Base.metadata.create_all(bind=engine)
app=FastAPI(title=settings.app_name,version="1.0.0",description="FitNexa fitness planning and optional AI coaching API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:3000",
        "http://localhost:3000",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def root(): return {"name":settings.app_name,"docs":"/docs","health":"/api/v1/health"}
@app.get("/api/v1/health")
def health(): return {"status":"ok","service":"FitNexa-api"}
@app.post("/api/v1/profiles",response_model=ProfileOut,status_code=201)
def create_profile(payload:ProfileCreate,db:Session=Depends(get_db)):
    profile=UserProfile(**payload.model_dump()); db.add(profile); db.commit(); db.refresh(profile); return profile
@app.get("/api/v1/profiles/{profile_id}",response_model=ProfileOut)
def get_profile(profile_id:int,db:Session=Depends(get_db)):
    profile=db.get(UserProfile,profile_id)
    if not profile: raise HTTPException(status_code=404,detail="Profile not found")
    return profile
@app.post("/api/v1/workouts/generate")
def generate_workout(payload:WorkoutRequest,db:Session=Depends(get_db)):
    plan=build_workout_plan(**payload.model_dump()); record=WorkoutPlan(goal=payload.goal,level=payload.level,days_per_week=payload.days_per_week,plan_json=json.dumps(plan)); db.add(record); db.commit(); db.refresh(record); return {"id":record.id,"plan":plan}
@app.post("/api/v1/nutrition/estimate")
def nutrition_estimate(payload:NutritionRequest): return estimate_nutrition(payload)
@app.post("/api/v1/coach/chat")
async def coach_chat(payload:CoachRequest): return await ai_coach_reply(payload.message.strip(),payload.goal)
@app.get("/api/v1/workouts/history")
def workout_history(limit:int=20,db:Session=Depends(get_db)):
    limit=max(1,min(limit,100)); rows=db.query(WorkoutPlan).order_by(WorkoutPlan.created_at.desc()).limit(limit).all()
    return [{"id":r.id,"goal":r.goal,"level":r.level,"days_per_week":r.days_per_week,"created_at":r.created_at.isoformat(),"plan":json.loads(r.plan_json)} for r in rows]
