from sqlalchemy.orm import Session
from models import HabitLog, Habit
from datetime import date, timedelta

def calculate_streak(db: Session, habit_id: int):
    habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if not habit:
        return None

    logs = db.query(HabitLog).filter(HabitLog.habit_id == habit_id).order_by(HabitLog.date.desc()).all()
    if not logs:
        return {
            "current_streak": 0,
            "longest_streak": 0,
            "missed_days": 0,
            "completion_percentage": 0.0
        }

    # Extract completed dates, sort ascending
    completed_dates = sorted([log.date for log in logs if log.completed])
    
    if not completed_dates:
        return {
            "current_streak": 0,
            "longest_streak": 0,
            "missed_days": len(logs),
            "completion_percentage": 0.0
        }

    # Current streak
    today = date.today()
    current_streak = 0
    check_date = completed_dates[-1]
    
    # Only active if log was today or yesterday
    if check_date == today or check_date == today - timedelta(days=1):
        current_streak = 1
        for i in range(len(completed_dates) - 2, -1, -1):
            if completed_dates[i] == check_date - timedelta(days=1):
                current_streak += 1
                check_date = completed_dates[i]
            else:
                break
    
    # Longest streak
    longest_streak = 1 if completed_dates else 0
    current_temp = 1 if completed_dates else 0
    for i in range(1, len(completed_dates)):
        if completed_dates[i] == completed_dates[i-1] + timedelta(days=1):
            current_temp += 1
            longest_streak = max(longest_streak, current_temp)
        else:
            current_temp = 1

    # Percentage
    start_date = habit.created_at.date()
    total_days = max((today - start_date).days + 1, 1)

    completed_days_count = len(completed_dates)
    missed_days = total_days - completed_days_count
    completion_percentage = (completed_days_count / total_days) * 100

    return {
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "missed_days": max(0, missed_days),
        "completion_percentage": round(completion_percentage, 2)
    }
