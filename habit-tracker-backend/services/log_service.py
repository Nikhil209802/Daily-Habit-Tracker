from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import HabitLog
from schemas import HabitLogCreate
from fastapi import HTTPException

def log_habit(db: Session, habit_id: int, log_data: HabitLogCreate):
    db_log = HabitLog(habit_id=habit_id, date=log_data.date, completed=log_data.completed)
    db.add(db_log)
    try:
        db.commit()
        db.refresh(db_log)
        return db_log
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Habit already logged for this date.")

def get_habit_logs(db: Session, habit_id: int):
    return db.query(HabitLog).filter(HabitLog.habit_id == habit_id).order_by(HabitLog.date.desc()).all()
