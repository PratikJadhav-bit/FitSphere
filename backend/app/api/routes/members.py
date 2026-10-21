"""Members CRUD API."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from typing import List, Optional
from app.database import get_db
from app import models, schemas
from datetime import datetime, date, timedelta
import random, string

router = APIRouter()


def _enrich_member(member: models.Member, db: Session) -> dict:
    membership = db.query(models.Membership).filter(
        models.Membership.member_id == member.id
    ).order_by(models.Membership.created_at.desc()).first()

    plan_name = None
    fitness_goal = None
    membership_status = "none"
    if membership:
        plan = db.query(models.Plan).filter(models.Plan.id == membership.plan_id).first()
        plan_name = plan.name if plan else None
        fitness_goal = membership.fitness_goal
        membership_status = membership.status

    total_sessions = db.query(models.Attendance).filter(
        models.Attendance.member_id == member.id
    ).count()

    last_30 = datetime.utcnow() - timedelta(days=30)
    checkins_30 = db.query(models.Attendance).filter(
        models.Attendance.member_id == member.id,
        models.Attendance.check_in >= last_30
    ).count()
    attendance_pct = min(round((checkins_30 / 30) * 100, 1), 100)

    return {
        "id": member.id,
        "full_name": member.full_name,
        "email": member.email,
        "phone": member.phone,
        "gender": member.gender,
        "date_of_birth": str(member.date_of_birth) if member.date_of_birth else None,
        "blood_group": member.blood_group,
        "avatar_color": member.avatar_color,
        "created_at": str(member.created_at),
        "membership_status": membership_status,
        "plan_name": plan_name,
        "fitness_goal": fitness_goal,
        "total_sessions": total_sessions,
        "attendance_pct": attendance_pct,
    }


@router.get("/", response_model=dict)
def list_members(
    skip: int = 0, limit: int = 20,
    status: Optional[str] = None,
    search: Optional[str] = None,
    plan: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Member)
    if search:
        q = f"%{search}%"
        query = query.filter(or_(
            models.Member.full_name.ilike(q),
            models.Member.email.ilike(q),
            models.Member.phone.ilike(q)
        ))
    total = query.count()
    members = query.order_by(models.Member.created_at.desc()).offset(skip).limit(limit).all()

    result = []
    for m in members:
        enriched = _enrich_member(m, db)
        if status and enriched["membership_status"] != status:
            continue
        if plan and enriched["plan_name"] != plan:
            continue
        result.append(enriched)

    return {"total": total, "items": result, "skip": skip, "limit": limit}


@router.post("/", response_model=dict, status_code=201)
def create_member(payload: schemas.MemberCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Member).filter(models.Member.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    member = models.Member(
        full_name=payload.full_name,
        email=payload.email,
        phone=payload.phone,
        gender=payload.gender,
        date_of_birth=payload.date_of_birth,
        blood_group=payload.blood_group,
        address=payload.address,
        emergency_contact=payload.emergency_contact,
        avatar_color=payload.avatar_color or "#3b82f6"
    )
    db.add(member)
    db.flush()

    if payload.plan_id:
        membership = models.Membership(
            member_id=member.id,
            plan_id=payload.plan_id,
            start_date=date.today(),
            end_date=date.today().replace(month=date.today().month % 12 + 1) if date.today().month < 12
                     else date(date.today().year + 1, 1, date.today().day),
            status="active",
            fitness_goal=payload.fitness_goal,
            assigned_trainer_id=payload.assigned_trainer_id
        )
        db.add(membership)

    db.commit()
    db.refresh(member)
    return _enrich_member(member, db)


@router.get("/{member_id}", response_model=dict)
def get_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(models.Member).filter(models.Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return _enrich_member(member, db)


@router.patch("/{member_id}", response_model=dict)
def update_member(member_id: int, payload: schemas.MemberUpdate, db: Session = Depends(get_db)):
    member = db.query(models.Member).filter(models.Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(member, field, value)
    member.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(member)
    return _enrich_member(member, db)


@router.delete("/{member_id}", status_code=204)
def delete_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(models.Member).filter(models.Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    db.delete(member)
    db.commit()
