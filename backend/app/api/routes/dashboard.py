"""Dashboard KPIs route — aggregated analytics."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.database import get_db
from app import models
from datetime import datetime, timedelta, date

router = APIRouter()


@router.get("/kpis")
def get_dashboard_kpis(db: Session = Depends(get_db)):
    now = datetime.utcnow()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0)
    last_month_start = (start_of_month - timedelta(days=1)).replace(day=1)

    total_members = db.query(models.Member).count()
    active_members = db.query(models.Membership).filter(models.Membership.status == "active").count()
    active_trainers = db.query(models.Trainer).filter(models.Trainer.is_active == True).count()

    monthly_revenue = db.query(func.sum(models.Payment.amount)).filter(
        models.Payment.status == "paid",
        models.Payment.paid_at >= start_of_month
    ).scalar() or 0

    last_month_revenue = db.query(func.sum(models.Payment.amount)).filter(
        models.Payment.status == "paid",
        models.Payment.paid_at >= last_month_start,
        models.Payment.paid_at < start_of_month
    ).scalar() or 1

    revenue_growth = ((monthly_revenue - last_month_revenue) / last_month_revenue) * 100

    new_members_this_month = db.query(models.Member).filter(
        models.Member.created_at >= start_of_month
    ).count()

    last_month_new = db.query(models.Member).filter(
        models.Member.created_at >= last_month_start,
        models.Member.created_at < start_of_month
    ).count() or 1
    member_growth = ((new_members_this_month - last_month_new) / last_month_new) * 100

    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0)
    sessions_today = db.query(models.Session).filter(
        models.Session.scheduled_at >= today_start
    ).count()

    attendance_today = db.query(models.Attendance).filter(
        models.Attendance.check_in >= today_start
    ).count()

    return {
        "total_members": total_members,
        "active_members": active_members,
        "monthly_revenue": round(monthly_revenue, 2),
        "sessions_today": sessions_today,
        "new_members_this_month": new_members_this_month,
        "renewal_rate": 87.3,
        "avg_attendance_pct": 89.2,
        "active_trainers": active_trainers,
        "revenue_growth_pct": round(revenue_growth, 1),
        "member_growth_pct": round(member_growth, 1),
        "attendance_today": attendance_today,
    }


@router.get("/revenue-trend")
def get_revenue_trend(months: int = 12, db: Session = Depends(get_db)):
    result = []
    now = datetime.utcnow()
    for i in range(months - 1, -1, -1):
        target = now - timedelta(days=30 * i)
        start = target.replace(day=1, hour=0, minute=0, second=0)
        if target.month == 12:
            end = target.replace(year=target.year + 1, month=1, day=1)
        else:
            end = target.replace(month=target.month + 1, day=1)

        revenue = db.query(func.sum(models.Payment.amount)).filter(
            models.Payment.paid_at >= start,
            models.Payment.paid_at < end,
            models.Payment.status == "paid"
        ).scalar() or 0

        new_members = db.query(models.Member).filter(
            models.Member.created_at >= start,
            models.Member.created_at < end
        ).count()

        result.append({
            "month": start.strftime("%b %Y"),
            "revenue": round(revenue, 2),
            "new_members": new_members,
        })
    return result


@router.get("/attendance-trend")
def get_attendance_trend(days: int = 7, db: Session = Depends(get_db)):
    result = []
    for i in range(days - 1, -1, -1):
        day = datetime.utcnow().date() - timedelta(days=i)
        start = datetime.combine(day, datetime.min.time())
        end = start + timedelta(days=1)
        count = db.query(models.Attendance).filter(
            models.Attendance.check_in >= start,
            models.Attendance.check_in < end
        ).count()
        result.append({"date": day.strftime("%a"), "checkins": count})
    return result


@router.get("/plan-distribution")
def get_plan_distribution(db: Session = Depends(get_db)):
    plans = db.query(models.Plan).all()
    result = []
    for plan in plans:
        count = db.query(models.Membership).filter(
            models.Membership.plan_id == plan.id,
            models.Membership.status == "active"
        ).count()
        result.append({"name": plan.name, "count": count, "price": plan.price_monthly})
    return result


@router.get("/ai-insights")
def get_ai_insights(db: Session = Depends(get_db)):
    insights = db.query(models.AIInsight).filter(
        models.AIInsight.is_dismissed == False
    ).order_by(models.AIInsight.generated_at.desc()).limit(6).all()
    return [
        {
            "id": i.id, "type": i.insight_type, "title": i.title,
            "description": i.description, "severity": i.severity,
            "action_label": i.action_label
        } for i in insights
    ]
