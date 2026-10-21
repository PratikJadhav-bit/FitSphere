"""
SQLAlchemy ORM Models — FitSphere Database
"""

from sqlalchemy import (
    Column, Integer, String, Float, Text, Date,
    DateTime, Boolean, ForeignKey, func
)
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class Plan(Base):
    __tablename__ = "plans"
    id              = Column(Integer, primary_key=True, index=True)
    name            = Column(String(50), unique=True, nullable=False)
    price_monthly   = Column(Float, nullable=False)
    price_quarterly = Column(Float)
    price_annual    = Column(Float)
    features        = Column(Text)        # JSON string
    max_sessions    = Column(Integer, default=-1)
    created_at      = Column(DateTime, default=datetime.utcnow)

    memberships     = relationship("Membership", back_populates="plan")


class Member(Base):
    __tablename__ = "members"
    id               = Column(Integer, primary_key=True, index=True)
    full_name        = Column(String(120), nullable=False)
    email            = Column(String(200), unique=True, nullable=False)
    phone            = Column(String(20), nullable=False)
    gender           = Column(String(10))
    date_of_birth    = Column(Date)
    blood_group      = Column(String(5))
    address          = Column(Text)
    emergency_contact= Column(String(100))
    avatar_color     = Column(String(50), default="#3b82f6")
    created_at       = Column(DateTime, default=datetime.utcnow)
    updated_at       = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    memberships      = relationship("Membership", back_populates="member", cascade="all, delete-orphan")
    attendance       = relationship("Attendance", back_populates="member", cascade="all, delete-orphan")
    measurements     = relationship("BodyMeasurement", back_populates="member", cascade="all, delete-orphan")
    meal_logs        = relationship("MealLog", back_populates="member", cascade="all, delete-orphan")
    payments         = relationship("Payment", back_populates="member", cascade="all, delete-orphan")


class Trainer(Base):
    __tablename__ = "trainers"
    id               = Column(Integer, primary_key=True, index=True)
    full_name        = Column(String(120), nullable=False)
    email            = Column(String(200), unique=True, nullable=False)
    phone            = Column(String(20))
    specialty        = Column(String(100), nullable=False)
    experience_years = Column(Integer, default=1)
    bio              = Column(Text)
    certifications   = Column(Text)      # JSON string
    rating           = Column(Float, default=5.0)
    total_reviews    = Column(Integer, default=0)
    hourly_rate      = Column(Float, default=500)
    avatar_gradient  = Column(String(200), default="linear-gradient(135deg,#3b82f6,#06b6d4)")
    is_active        = Column(Boolean, default=True)
    joined_date      = Column(Date, default=func.current_date())
    created_at       = Column(DateTime, default=datetime.utcnow)

    sessions         = relationship("Session", back_populates="trainer")
    memberships      = relationship("Membership", back_populates="assigned_trainer")


class Membership(Base):
    __tablename__ = "memberships"
    id               = Column(Integer, primary_key=True, index=True)
    member_id        = Column(Integer, ForeignKey("members.id", ondelete="CASCADE"), nullable=False)
    plan_id          = Column(Integer, ForeignKey("plans.id"), nullable=False)
    start_date       = Column(Date, nullable=False)
    end_date         = Column(Date, nullable=False)
    status           = Column(String(20), default="active")
    fitness_goal     = Column(String(50))
    assigned_trainer_id = Column(Integer, ForeignKey("trainers.id"))
    created_at       = Column(DateTime, default=datetime.utcnow)

    member           = relationship("Member", back_populates="memberships")
    plan             = relationship("Plan", back_populates="memberships")
    assigned_trainer = relationship("Trainer", back_populates="memberships")


class Attendance(Base):
    __tablename__ = "attendance"
    id               = Column(Integer, primary_key=True, index=True)
    member_id        = Column(Integer, ForeignKey("members.id", ondelete="CASCADE"), nullable=False)
    check_in         = Column(DateTime, nullable=False, default=datetime.utcnow)
    check_out        = Column(DateTime)
    duration_minutes = Column(Integer)
    workout_type     = Column(String(50))
    calories_burned  = Column(Integer)
    notes            = Column(Text)
    created_at       = Column(DateTime, default=datetime.utcnow)

    member           = relationship("Member", back_populates="attendance")


class Session(Base):
    __tablename__ = "sessions"
    id               = Column(Integer, primary_key=True, index=True)
    trainer_id       = Column(Integer, ForeignKey("trainers.id"), nullable=False)
    title            = Column(String(150), nullable=False)
    session_type     = Column(String(20))
    scheduled_at     = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, default=60)
    max_capacity     = Column(Integer, default=1)
    current_enrolled = Column(Integer, default=0)
    status           = Column(String(20), default="scheduled")
    location         = Column(String(100), default="Main Gym Floor")
    price            = Column(Float, default=0)
    created_at       = Column(DateTime, default=datetime.utcnow)

    trainer          = relationship("Trainer", back_populates="sessions")


class BodyMeasurement(Base):
    __tablename__ = "body_measurements"
    id               = Column(Integer, primary_key=True, index=True)
    member_id        = Column(Integer, ForeignKey("members.id", ondelete="CASCADE"), nullable=False)
    measured_at      = Column(Date, nullable=False)
    weight_kg        = Column(Float)
    height_cm        = Column(Float)
    body_fat_pct     = Column(Float)
    muscle_mass_kg   = Column(Float)
    bmi              = Column(Float)
    chest_cm         = Column(Float)
    waist_cm         = Column(Float)
    hips_cm          = Column(Float)
    arms_cm          = Column(Float)
    thighs_cm        = Column(Float)
    notes            = Column(Text)
    created_at       = Column(DateTime, default=datetime.utcnow)

    member           = relationship("Member", back_populates="measurements")


class MealLog(Base):
    __tablename__ = "meal_logs"
    id               = Column(Integer, primary_key=True, index=True)
    member_id        = Column(Integer, ForeignKey("members.id", ondelete="CASCADE"), nullable=False)
    meal_type        = Column(String(20))
    food_items       = Column(Text, nullable=False)
    calories         = Column(Integer)
    protein_g        = Column(Float)
    carbs_g          = Column(Float)
    fats_g           = Column(Float)
    water_ml         = Column(Integer, default=0)
    logged_at        = Column(DateTime, default=datetime.utcnow)
    notes            = Column(Text)

    member           = relationship("Member", back_populates="meal_logs")


class Payment(Base):
    __tablename__ = "payments"
    id               = Column(Integer, primary_key=True, index=True)
    member_id        = Column(Integer, ForeignKey("members.id", ondelete="CASCADE"), nullable=False)
    membership_id    = Column(Integer, ForeignKey("memberships.id"))
    amount           = Column(Float, nullable=False)
    payment_method   = Column(String(20))
    transaction_ref  = Column(String(100), unique=True)
    status           = Column(String(20), default="paid")
    paid_at          = Column(DateTime, default=datetime.utcnow)
    notes            = Column(Text)

    member           = relationship("Member", back_populates="payments")


class Reminder(Base):
    __tablename__ = "reminders"
    id               = Column(Integer, primary_key=True, index=True)
    title            = Column(String(200), nullable=False)
    description      = Column(Text)
    reminder_type    = Column(String(30))
    target_member_id = Column(Integer, ForeignKey("members.id"))
    scheduled_at     = Column(DateTime, nullable=False)
    is_sent          = Column(Boolean, default=False)
    is_active        = Column(Boolean, default=True)
    channel          = Column(String(20), default="app")
    created_at       = Column(DateTime, default=datetime.utcnow)


class AIInsight(Base):
    __tablename__ = "ai_insights"
    id             = Column(Integer, primary_key=True, index=True)
    insight_type   = Column(String(50), nullable=False)
    title          = Column(String(200), nullable=False)
    description    = Column(Text, nullable=False)
    severity       = Column(String(20), default="info")
    action_label   = Column(String(100))
    is_dismissed   = Column(Boolean, default=False)
    generated_at   = Column(DateTime, default=datetime.utcnow)
