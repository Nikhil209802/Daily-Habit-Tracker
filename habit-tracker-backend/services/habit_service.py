from sqlalchemy.orm import Session
from models import Habit
from schemas import HabitCreate, HabitUpdate

def create_habit(db: Session, habit: HabitCreate, user_id: int):
    db_habit = Habit(**habit.model_dump(), user_id=user_id)
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit

def get_habit(db: Session, habit_id: int):
    return db.query(Habit).filter(Habit.id == habit_id).first()

def get_user_habits(db: Session, user_id: int):
    return db.query(Habit).filter(Habit.user_id == user_id).all()

def update_habit(db: Session, habit_id: int, habit_update: HabitUpdate):
    db_habit = get_habit(db, habit_id)
    if not db_habit:
        return None
    
    update_data = habit_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_habit, key, value)
        
    db.commit()
    db.refresh(db_habit)
    return db_habit

def delete_habit(db: Session, habit_id: int):
    db_habit = get_habit(db, habit_id)
    if db_habit:
        db.delete(db_habit)
        db.commit()
        return True
    return False
