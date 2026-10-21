"""Diet & Meal logging routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app import models, schemas
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/member/{member_id}/today")
def get_today_meals(member_id: int, db: Session = Depends(get_db)):
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0)
    meals = db.query(models.MealLog).filter(
        models.MealLog.member_id == member_id,
        models.MealLog.logged_at >= today_start
    ).order_by(models.MealLog.logged_at).all()
    total_cals = sum(m.calories or 0 for m in meals)
    total_protein = sum(m.protein_g or 0 for m in meals)
    total_carbs = sum(m.carbs_g or 0 for m in meals)
    total_fats = sum(m.fats_g or 0 for m in meals)
    total_water = sum(m.water_ml or 0 for m in meals)
    return {
        "meals": [{"id": m.id, "meal_type": m.meal_type, "food_items": m.food_items,
                   "calories": m.calories, "protein_g": m.protein_g,
                   "carbs_g": m.carbs_g, "fats_g": m.fats_g,
                   "water_ml": m.water_ml, "logged_at": str(m.logged_at)} for m in meals],
        "totals": {"calories": total_cals, "protein_g": total_protein,
                   "carbs_g": total_carbs, "fats_g": total_fats, "water_ml": total_water},
        "targets": {"calories": 2200, "protein_g": 180, "carbs_g": 240, "fats_g": 65, "water_ml": 3000}
    }

@router.post("/", status_code=201)
def log_meal(payload: schemas.MealLogCreate, db: Session = Depends(get_db)):
    meal = models.MealLog(**payload.dict())
    db.add(meal)
    db.commit()
    db.refresh(meal)
    return meal

@router.get("/recommendations/{member_id}")
def get_diet_recommendations(member_id: int, db: Session = Depends(get_db)):
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0)
    meals = db.query(models.MealLog).filter(
        models.MealLog.member_id == member_id,
        models.MealLog.logged_at >= today_start
    ).all()
    protein = sum(m.protein_g or 0 for m in meals)
    water = sum(m.water_ml or 0 for m in meals)
    cals = sum(m.calories or 0 for m in meals)

    recs = []
    if protein < 130:
        recs.append({"icon": "🥩", "text": f"Add {180 - protein:.0f}g more protein today. Try grilled chicken, eggs or cottage cheese.", "priority": "high"})
    if water < 2000:
        recs.append({"icon": "💧", "text": f"You're {3000 - water}ml below water target. Drink 2 glasses before your next meal.", "priority": "medium"})
    if cals < 1500:
        recs.append({"icon": "🔥", "text": "Caloric intake is below target. Add a nutrient-dense snack to fuel your recovery.", "priority": "medium"})
    if cals > 2400:
        recs.append({"icon": "⚠️", "text": "You've exceeded your calorie target. Consider a lighter dinner.", "priority": "high"})
    recs.append({"icon": "🌿", "text": "Great job including greens in your diet! Aim for 5+ servings of fruits/vegetables.", "priority": "low"})
    return recs
