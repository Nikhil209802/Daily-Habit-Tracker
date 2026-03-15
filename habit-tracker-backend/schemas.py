from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, date
from typing import List, Optional

# --- User Schemas ---
class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# --- Habit Schemas ---
class HabitBase(BaseModel):
    habit_name: str
    category: Optional[str] = None
    target_frequency: str = Field("daily", pattern="^(daily|weekly)$")

class HabitCreate(HabitBase):
    pass

class HabitUpdate(BaseModel):
    habit_name: Optional[str] = None
    category: Optional[str] = None
    target_frequency: Optional[str] = Field(None, pattern="^(daily|weekly)$")

class HabitResponse(HabitBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# --- HabitLog Schemas ---
class HabitLogBase(BaseModel):
    date: date
    completed: bool = True

class HabitLogCreate(HabitLogBase):
    pass

class HabitLogResponse(HabitLogBase):
    id: int
    habit_id: int
    
    class Config:
        from_attributes = True

# --- Analytics Schemas ---
class StreakInfo(BaseModel):
    current_streak: int
    longest_streak: int
    missed_days: int
    completion_percentage: float

class WeeklyData(BaseModel):
    date: date
    completed: bool

class CountData(BaseModel):
    date: date
    count: int
