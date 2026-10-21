"""Revenue & Payments routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app import models, schemas
from datetime import datetime, timedelta
import uuid

router = APIRouter()

@router.get("/summary")
def revenue_summary(db: Session = Depends(get_db)):
    now = datetime.utcnow()
    start = now.replace(day=1, hour=0, minute=0, second=0)
    last_start = (start - timedelta(days=1)).replace(day=1)

    month_rev = db.query(func.sum(models.Payment.amount)).filter(
        models.Payment.status == "paid", models.Payment.paid_at >= start
    ).scalar() or 0
    last_rev = db.query(func.sum(models.Payment.amount)).filter(
        models.Payment.status == "paid",
        models.Payment.paid_at >= last_start, models.Payment.paid_at < start
    ).scalar() or 1

    annual_rev = db.query(func.sum(models.Payment.amount)).filter(
        models.Payment.status == "paid",
        models.Payment.paid_at >= now.replace(month=1, day=1, hour=0)
    ).scalar() or 0

    total_members = db.query(models.Member).count() or 1
    rev_per_member = month_rev / total_members

    return {
        "monthly_revenue": round(month_rev, 2),
        "last_month_revenue": round(last_rev, 2),
        "growth_pct": round(((month_rev - last_rev) / last_rev) * 100, 1),
        "annual_revenue": round(annual_rev, 2),
        "revenue_per_member": round(rev_per_member, 2),
        "forecast_next_month": round(month_rev * 1.12, 2),
    }

@router.get("/transactions")
def list_transactions(limit: int = 20, db: Session = Depends(get_db)):
    payments = db.query(models.Payment).order_by(models.Payment.paid_at.desc()).limit(limit).all()
    result = []
    for p in payments:
        member = db.query(models.Member).filter(models.Member.id == p.member_id).first()
        result.append({
            "id": p.id, "member_name": member.full_name if member else "Unknown",
            "amount": p.amount, "method": p.payment_method,
            "status": p.status, "paid_at": str(p.paid_at),
            "transaction_ref": p.transaction_ref,
        })
    return result

@router.post("/", status_code=201)
def create_payment(payload: schemas.PaymentCreate, db: Session = Depends(get_db)):
    payment = models.Payment(
        member_id=payload.member_id,
        amount=payload.amount,
        payment_method=payload.payment_method,
        transaction_ref=f"TXN-{uuid.uuid4().hex[:10].upper()}",
        status="paid",
        notes=payload.notes
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment

@router.get("/trend")
def revenue_trend(months: int = 12, db: Session = Depends(get_db)):
    now = datetime.utcnow()
    result = []
    for i in range(months - 1, -1, -1):
        target = now - timedelta(days=30 * i)
        start = target.replace(day=1, hour=0, minute=0, second=0)
        end = (start + timedelta(days=32)).replace(day=1)
        rev = db.query(func.sum(models.Payment.amount)).filter(
            models.Payment.paid_at >= start,
            models.Payment.paid_at < end,
            models.Payment.status == "paid"
        ).scalar() or 0
        result.append({"month": start.strftime("%b"), "revenue": round(rev, 2)})
    return result
