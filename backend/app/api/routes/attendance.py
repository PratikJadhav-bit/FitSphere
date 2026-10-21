"""Attendance tracking routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app import models, schemas
from datetime import datetime, timedelta, date

router = APIRouter()


@router.get("/today")
def get_today_attendance(db: Session = Depends(get_db)):
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    records = db.query(models.Attendance).filter(
        models.Attendance.check_in >= today_start
    ).order_by(models.Attendance.check_in.desc()).limit(50).all()

    result = []
    for r in records:
        member = db.query(models.Member).filter(models.Member.id == r.member_id).first()
        result.append({
            "id": r.id, "member_id": r.member_id,
            "member_name": member.full_name if member else "Unknown",
            "avatar_color": member.avatar_color if member else "#3b82f6",
            "check_in": str(r.check_in), "check_out": str(r.check_out) if r.check_out else None,
            "duration_minutes": r.duration_minutes, "workout_type": r.workout_type,
            "calories_burned": r.calories_burned,
        })
    return result


@router.post("/checkin", status_code=201)
def check_in(payload: schemas.AttendanceCreate, db: Session = Depends(get_db)):
    member = db.query(models.Member).filter(models.Member.id == payload.member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    today = datetime.utcnow().replace(hour=0, minute=0, second=0)
    existing = db.query(models.Attendance).filter(
        models.Attendance.member_id == payload.member_id,
        models.Attendance.check_in >= today,
        models.Attendance.check_out == None
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Member already checked in")

    record = models.Attendance(
        member_id=payload.member_id,
        check_in=payload.check_in or datetime.utcnow(),
        workout_type=payload.workout_type,
        notes=payload.notes
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return {"id": record.id, "member_name": member.full_name, "check_in": str(record.check_in)}


@router.patch("/{attendance_id}/checkout")
def check_out(attendance_id: int, db: Session = Depends(get_db)):
    record = db.query(models.Attendance).filter(models.Attendance.id == attendance_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    record.check_out = datetime.utcnow()
    delta = record.check_out - record.check_in
    record.duration_minutes = int(delta.total_seconds() / 60)
    record.calories_burned = record.duration_minutes * 7  # estimate
    db.commit()
    return {"duration_minutes": record.duration_minutes, "calories_burned": record.calories_burned}


@router.get("/stats")
def attendance_stats(db: Session = Depends(get_db)):
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0)
    today_count = db.query(models.Attendance).filter(models.Attendance.check_in >= today_start).count()
    avg_duration = db.query(func.avg(models.Attendance.duration_minutes)).scalar() or 0
    last_7 = datetime.utcnow() - timedelta(days=7)
    weekly_count = db.query(models.Attendance).filter(models.Attendance.check_in >= last_7).count()
    return {
        "today": today_count,
        "avg_duration_minutes": round(avg_duration, 0),
        "weekly_total": weekly_count,
        "avg_per_day": round(weekly_count / 7, 1),
    }


@router.get("/hourly")
def hourly_distribution(db: Session = Depends(get_db)):
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0)
    result = []
    for hour in range(24):
        start = today_start.replace(hour=hour)
        end = today_start.replace(hour=(hour + 1) % 24) if hour < 23 else today_start + timedelta(days=1)
        count = db.query(models.Attendance).filter(
            models.Attendance.check_in >= start,
            models.Attendance.check_in < end
        ).count()
        label = f"{hour:02d}:00"
        result.append({"hour": label, "count": count})
    return result


@router.get("/member/{member_id}/history")
def member_attendance_history(member_id: int, days: int = 30, db: Session = Depends(get_db)):
    since = datetime.utcnow() - timedelta(days=days)
    records = db.query(models.Attendance).filter(
        models.Attendance.member_id == member_id,
        models.Attendance.check_in >= since
    ).order_by(models.Attendance.check_in.desc()).all()
    return [
        {
            "date": r.check_in.strftime("%Y-%m-%d"),
            "duration_minutes": r.duration_minutes,
            "workout_type": r.workout_type,
            "calories_burned": r.calories_burned,
        } for r in records
    ]
