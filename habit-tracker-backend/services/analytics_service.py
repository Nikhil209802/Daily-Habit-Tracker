from sqlalchemy.orm import Session
from sqlalchemy import func
from models import HabitLog, Habit
from datetime import date, timedelta
from typing import List
from schemas import WeeklyData, CountData
from services.streak_service import calculate_streak

def get_weekly_analytics(db: Session, habit_id: int):
    today = date.today()
    start_date = today - timedelta(days=6)
    logs = db.query(HabitLog).filter(
        HabitLog.habit_id == habit_id,
        HabitLog.date >= start_date,
        HabitLog.date <= today
    ).all()
    
    log_map = {log.date: log.completed for log in logs}
    
    weekly_data = []
    for i in range(7):
        current_date = start_date + timedelta(days=i)
        weekly_data.append(WeeklyData(date=current_date, completed=log_map.get(current_date, False)))
        
    return weekly_data

def get_monthly_analytics(db: Session, habit_id: int):
    today = date.today()
    start_date = today - timedelta(days=29)
    logs = db.query(HabitLog).filter(
        HabitLog.habit_id == habit_id,
        HabitLog.date >= start_date,
        HabitLog.date <= today
    ).all()
    
    log_map = {log.date: log.completed for log in logs}
    
    monthly_data = []
    for i in range(30):
        current_date = start_date + timedelta(days=i)
        monthly_data.append(WeeklyData(date=current_date, completed=log_map.get(current_date, False)))
        
    return monthly_data

def get_consistency(db: Session, habit_id: int):
    streak_info = calculate_streak(db, habit_id)
    if not streak_info:
        return {"completion_percentage": 0.0}
    return {"completion_percentage": streak_info["completion_percentage"]}

def get_heatmap_data(db: Session, user_id: int):
    results = db.query(
        HabitLog.date,
        func.count(HabitLog.id).label('count')
    ).join(Habit).filter(
        Habit.user_id == user_id,
        HabitLog.completed == True
    ).group_by(HabitLog.date).all()
    
    return [CountData(date=r.date, count=r.count) for r in results]
