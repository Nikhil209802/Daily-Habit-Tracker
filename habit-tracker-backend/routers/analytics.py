from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from schemas import StreakInfo, WeeklyData, CountData
from database import get_db
from services import analytics_service, streak_service

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/streak/{habit_id}", response_model=StreakInfo)
def get_streak(habit_id: int, db: Session = Depends(get_db)):
    streak_info = streak_service.calculate_streak(db, habit_id)
    if not streak_info:
        raise HTTPException(status_code=404, detail="Habit not found")
    return streak_info

@router.get("/weekly/{habit_id}", response_model=List[WeeklyData])
def get_weekly(habit_id: int, db: Session = Depends(get_db)):
    return analytics_service.get_weekly_analytics(db, habit_id)

@router.get("/monthly/{habit_id}", response_model=List[WeeklyData])
def get_monthly(habit_id: int, db: Session = Depends(get_db)):
    return analytics_service.get_monthly_analytics(db, habit_id)

@router.get("/consistency/{habit_id}")
def get_consistency_rate(habit_id: int, db: Session = Depends(get_db)):
    return analytics_service.get_consistency(db, habit_id)

@router.get("/heatmap/{user_id}", response_model=List[CountData])
def get_heatmap(user_id: int, db: Session = Depends(get_db)):
    return analytics_service.get_heatmap_data(db, user_id)
