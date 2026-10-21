"""Pydantic schemas for request/response validation."""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date, datetime


# ── Plan Schemas ──────────────────────────────────────────────────
class PlanBase(BaseModel):
    name: str
    price_monthly: float
    price_quarterly: Optional[float] = None
    price_annual: Optional[float] = None
    features: Optional[str] = None
    max_sessions: int = -1

class PlanRead(PlanBase):
    id: int
    created_at: datetime
    class Config: from_attributes = True


# ── Member Schemas ────────────────────────────────────────────────
class MemberCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=120)
    email: str
    phone: str = Field(..., min_length=7)
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None
    blood_group: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    avatar_color: Optional[str] = "#3b82f6"
    plan_id: Optional[int] = None
    fitness_goal: Optional[str] = None
    assigned_trainer_id: Optional[int] = None

class MemberUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None

class MemberRead(BaseModel):
    id: int
    full_name: str
    email: str
    phone: str
    gender: Optional[str]
    date_of_birth: Optional[date]
    blood_group: Optional[str]
    avatar_color: Optional[str]
    created_at: datetime
    membership_status: Optional[str] = None
    plan_name: Optional[str] = None
    fitness_goal: Optional[str] = None
    total_sessions: Optional[int] = 0
    attendance_pct: Optional[float] = 0.0
    class Config: from_attributes = True


# ── Trainer Schemas ───────────────────────────────────────────────
class TrainerCreate(BaseModel):
    full_name: str
    email: str
    phone: Optional[str] = None
    specialty: str
    experience_years: int = 1
    bio: Optional[str] = None
    certifications: Optional[str] = None
    hourly_rate: float = 500
    avatar_gradient: Optional[str] = "linear-gradient(135deg,#3b82f6,#06b6d4)"

class TrainerRead(BaseModel):
    id: int
    full_name: str
    email: str
    phone: Optional[str]
    specialty: str
    experience_years: int
    bio: Optional[str]
    certifications: Optional[str]
    rating: float
    total_reviews: int
    hourly_rate: float
    avatar_gradient: str
    is_active: bool
    joined_date: Optional[date]
    total_members: Optional[int] = 0
    class Config: from_attributes = True


# ── Attendance Schemas ────────────────────────────────────────────
class AttendanceCreate(BaseModel):
    member_id: int
    check_in: Optional[datetime] = None
    workout_type: Optional[str] = None
    notes: Optional[str] = None

class AttendanceRead(BaseModel):
    id: int
    member_id: int
    member_name: Optional[str] = None
    check_in: datetime
    check_out: Optional[datetime]
    duration_minutes: Optional[int]
    workout_type: Optional[str]
    calories_burned: Optional[int]
    class Config: from_attributes = True


# ── Session Schemas ───────────────────────────────────────────────
class SessionCreate(BaseModel):
    trainer_id: int
    title: str
    session_type: str = "Group"
    scheduled_at: datetime
    duration_minutes: int = 60
    max_capacity: int = 10
    location: str = "Main Gym Floor"
    price: float = 0

class SessionRead(BaseModel):
    id: int
    trainer_id: int
    trainer_name: Optional[str] = None
    title: str
    session_type: str
    scheduled_at: datetime
    duration_minutes: int
    max_capacity: int
    current_enrolled: int
    status: str
    location: str
    price: float
    class Config: from_attributes = True


# ── Body Measurement Schemas ──────────────────────────────────────
class MeasurementCreate(BaseModel):
    member_id: int
    measured_at: date
    weight_kg: Optional[float] = None
    height_cm: Optional[float] = None
    body_fat_pct: Optional[float] = None
    muscle_mass_kg: Optional[float] = None
    chest_cm: Optional[float] = None
    waist_cm: Optional[float] = None
    hips_cm: Optional[float] = None
    arms_cm: Optional[float] = None
    thighs_cm: Optional[float] = None
    notes: Optional[str] = None

class MeasurementRead(MeasurementCreate):
    id: int
    bmi: Optional[float]
    created_at: datetime
    class Config: from_attributes = True


# ── Meal Log Schemas ──────────────────────────────────────────────
class MealLogCreate(BaseModel):
    member_id: int
    meal_type: str
    food_items: str
    calories: Optional[int] = None
    protein_g: Optional[float] = None
    carbs_g: Optional[float] = None
    fats_g: Optional[float] = None
    water_ml: int = 0
    notes: Optional[str] = None

class MealLogRead(MealLogCreate):
    id: int
    logged_at: datetime
    class Config: from_attributes = True


# ── Payment Schemas ───────────────────────────────────────────────
class PaymentCreate(BaseModel):
    member_id: int
    amount: float
    payment_method: str = "UPI"
    notes: Optional[str] = None

class PaymentRead(BaseModel):
    id: int
    member_id: int
    member_name: Optional[str] = None
    amount: float
    payment_method: Optional[str]
    transaction_ref: Optional[str]
    status: str
    paid_at: datetime
    plan_name: Optional[str] = None
    class Config: from_attributes = True


# ── Reminder Schemas ──────────────────────────────────────────────
class ReminderCreate(BaseModel):
    title: str
    description: Optional[str] = None
    reminder_type: str = "custom"
    target_member_id: Optional[int] = None
    scheduled_at: datetime
    channel: str = "app"

class ReminderRead(ReminderCreate):
    id: int
    is_sent: bool
    is_active: bool
    created_at: datetime
    member_name: Optional[str] = None
    class Config: from_attributes = True


# ── Dashboard KPIs ────────────────────────────────────────────────
class DashboardKPIs(BaseModel):
    total_members: int
    active_members: int
    monthly_revenue: float
    sessions_today: int
    new_members_this_month: int
    renewal_rate: float
    avg_attendance_pct: float
    active_trainers: int
    revenue_growth_pct: float
    member_growth_pct: float

class AIMessage(BaseModel):
    message: str
    context: Optional[str] = None
