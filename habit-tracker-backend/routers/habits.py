from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas import HabitCreate, HabitUpdate, HabitResponse, HabitLogCreate, HabitLogResponse
from database import get_db
from services import habit_service, log_service

router = APIRouter(prefix="/habits", tags=["habits"])

@router.post("/", response_model=HabitResponse)
def create_habit(habit: HabitCreate, user_id: int, db: Session = Depends(get_db)):
    return habit_service.create_habit(db=db, habit=habit, user_id=user_id)

@router.get("/{user_id}", response_model=List[HabitResponse])
def get_user_habits(user_id: int, db: Session = Depends(get_db)):
    # Note: user_id provided as path parameter instead of GET /habits/user/{user_id}
    # User might need a dedicated router.
    return habit_service.get_user_habits(db, user_id=user_id)

@router.put("/{habit_id}", response_model=HabitResponse)
def update_habit(habit_id: int, habit: HabitUpdate, db: Session = Depends(get_db)):
    db_habit = habit_service.update_habit(db, habit_id, habit)
    if not db_habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return db_habit

@router.delete("/{habit_id}")
def delete_habit(habit_id: int, db: Session = Depends(get_db)):
    success = habit_service.delete_habit(db, habit_id)
    if not success:
        raise HTTPException(status_code=404, detail="Habit not found")
    return {"message": "Habit deleted successfully"}

@router.post("/{habit_id}/mark", response_model=HabitLogResponse)
def mark_habit(habit_id: int, log_data: HabitLogCreate, db: Session = Depends(get_db)):
    habit = habit_service.get_habit(db, habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return log_service.log_habit(db, habit_id, log_data)

@router.get("/{habit_id}/history", response_model=List[HabitLogResponse])
def get_habit_history(habit_id: int, db: Session = Depends(get_db)):
    return log_service.get_habit_logs(db, habit_id)
