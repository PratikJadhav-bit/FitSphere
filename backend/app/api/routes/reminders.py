"""Reminders management routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from datetime import datetime

router = APIRouter()

@router.get("/")
def list_reminders(db: Session = Depends(get_db)):
    reminders = db.query(models.Reminder).filter(
        models.Reminder.is_active == True
    ).order_by(models.Reminder.scheduled_at).all()
    result = []
    for r in reminders:
        member_name = None
        if r.target_member_id:
            m = db.query(models.Member).filter(models.Member.id == r.target_member_id).first()
            member_name = m.full_name if m else None
        result.append({
            "id": r.id, "title": r.title, "description": r.description,
            "reminder_type": r.reminder_type, "scheduled_at": str(r.scheduled_at),
            "is_sent": r.is_sent, "channel": r.channel, "member_name": member_name,
        })
    return result

@router.post("/", status_code=201)
def create_reminder(payload: schemas.ReminderCreate, db: Session = Depends(get_db)):
    reminder = models.Reminder(**payload.dict())
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder

@router.delete("/{reminder_id}", status_code=204)
def delete_reminder(reminder_id: int, db: Session = Depends(get_db)):
    r = db.query(models.Reminder).filter(models.Reminder.id == reminder_id).first()
    if not r:
        raise HTTPException(404, "Reminder not found")
    r.is_active = False
    db.commit()
