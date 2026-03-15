from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    habits = relationship("Habit", back_populates="user", cascade="all, delete")

class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    habit_name = Column(String, index=True)
    category = Column(String)
    target_frequency = Column(String, default="daily") # daily, weekly
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="habits")
    logs = relationship("HabitLog", back_populates="habit", cascade="all, delete")

class HabitLog(Base):
    __tablename__ = "habit_logs"

    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id"))
    date = Column(Date, index=True)
    completed = Column(Boolean, default=False)
    
    habit = relationship("Habit", back_populates="logs")

    __table_args__ = (
        UniqueConstraint('habit_id', 'date', name='uq_habit_date'),
    )
