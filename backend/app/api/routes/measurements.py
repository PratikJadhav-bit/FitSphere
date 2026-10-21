"""Body measurements routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter()

@router.get("/member/{member_id}")
def get_measurements(member_id: int, db: Session = Depends(get_db)):
    records = db.query(models.BodyMeasurement).filter(
        models.BodyMeasurement.member_id == member_id
    ).order_by(models.BodyMeasurement.measured_at.desc()).all()
    return [
        {
            "id": r.id, "measured_at": str(r.measured_at),
            "weight_kg": r.weight_kg, "body_fat_pct": r.body_fat_pct,
            "muscle_mass_kg": r.muscle_mass_kg, "bmi": r.bmi,
            "chest_cm": r.chest_cm, "waist_cm": r.waist_cm,
            "hips_cm": r.hips_cm, "arms_cm": r.arms_cm,
        } for r in records
    ]

@router.post("/", status_code=201)
def log_measurement(payload: schemas.MeasurementCreate, db: Session = Depends(get_db)):
    bmi = None
    if payload.weight_kg and payload.height_cm:
        h = payload.height_cm / 100
        bmi = round(payload.weight_kg / (h * h), 1)
    measurement = models.BodyMeasurement(**payload.dict(), bmi=bmi)
    db.add(measurement)
    db.commit()
    db.refresh(measurement)
    return measurement
