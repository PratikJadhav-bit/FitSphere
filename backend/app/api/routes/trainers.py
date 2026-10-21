"""Trainers management routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter()

@router.get("/")
def list_trainers(db: Session = Depends(get_db)):
    trainers = db.query(models.Trainer).filter(models.Trainer.is_active == True).all()
    result = []
    for t in trainers:
        members_count = db.query(models.Membership).filter(
            models.Membership.assigned_trainer_id == t.id,
            models.Membership.status == "active"
        ).count()
        result.append({
            "id": t.id, "full_name": t.full_name, "email": t.email,
            "phone": t.phone, "specialty": t.specialty,
            "experience_years": t.experience_years, "bio": t.bio,
            "certifications": t.certifications, "rating": t.rating,
            "total_reviews": t.total_reviews, "hourly_rate": t.hourly_rate,
            "avatar_gradient": t.avatar_gradient, "is_active": t.is_active,
            "joined_date": str(t.joined_date) if t.joined_date else None,
            "total_members": members_count,
        })
    return result

@router.post("/", status_code=201)
def create_trainer(payload: schemas.TrainerCreate, db: Session = Depends(get_db)):
    trainer = models.Trainer(**payload.dict())
    db.add(trainer)
    db.commit()
    db.refresh(trainer)
    return trainer

@router.get("/{trainer_id}")
def get_trainer(trainer_id: int, db: Session = Depends(get_db)):
    trainer = db.query(models.Trainer).filter(models.Trainer.id == trainer_id).first()
    if not trainer:
        raise HTTPException(404, "Trainer not found")
    return trainer
