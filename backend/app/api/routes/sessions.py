"""Sessions scheduling routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession
from app.database import get_db
from app import models, schemas
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/")
def list_sessions(date: str = None, db: DBSession = Depends(get_db)):
    query = db.query(models.Session)
    if date:
        dt = datetime.strptime(date, "%Y-%m-%d")
        query = query.filter(
            models.Session.scheduled_at >= dt,
            models.Session.scheduled_at < dt + timedelta(days=1)
        )
    sessions = query.order_by(models.Session.scheduled_at).limit(50).all()
    result = []
    for s in sessions:
        trainer = db.query(models.Trainer).filter(models.Trainer.id == s.trainer_id).first()
        result.append({
            "id": s.id, "title": s.title,
            "trainer_name": trainer.full_name if trainer else "TBA",
            "session_type": s.session_type,
            "scheduled_at": str(s.scheduled_at),
            "duration_minutes": s.duration_minutes,
            "max_capacity": s.max_capacity,
            "current_enrolled": s.current_enrolled,
            "status": s.status, "location": s.location, "price": s.price,
        })
    return result

@router.post("/", status_code=201)
def create_session(payload: schemas.SessionCreate, db: DBSession = Depends(get_db)):
    session = models.Session(**payload.dict())
    db.add(session)
    db.commit()
    db.refresh(session)
    return session
