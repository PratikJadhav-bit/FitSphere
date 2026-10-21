"""
FitSphere Database Seeder
=========================
Populates the database with realistic seed data for demo/development.
Run: python seed_db.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal, engine, Base
from app import models
from datetime import datetime, date, timedelta
import random
import uuid

Base.metadata.create_all(bind=engine)
db = SessionLocal()

print("🌱 Seeding FitSphere database...")

# ── Plans ─────────────────────────────────────────────────────
plans_data = [
    {"name": "Basic", "price_monthly": 999, "price_quarterly": 2699, "price_annual": 9599,
     "features": '["Gym Access","Locker Room","2 Group Classes/Month"]', "max_sessions": 2},
    {"name": "Pro", "price_monthly": 1999, "price_quarterly": 5399, "price_annual": 19199,
     "features": '["Unlimited Gym Access","All Group Classes","1 PT Session/Month","Diet Consultation"]', "max_sessions": -1},
    {"name": "Elite", "price_monthly": 3499, "price_quarterly": 9449, "price_annual": 33599,
     "features": '["Everything in Pro","4 PT Sessions/Month","Nutrition Plan","Body Assessment","Priority Booking","Sauna Access"]', "max_sessions": -1},
]
for p in plans_data:
    existing = db.query(models.Plan).filter(models.Plan.name == p["name"]).first()
    if not existing:
        db.add(models.Plan(**p))
db.commit()
print("  ✅ Plans seeded")

plans = db.query(models.Plan).all()
plan_map = {p.name: p.id for p in plans}

# ── Trainers ──────────────────────────────────────────────────
trainers_data = [
    {"full_name": "Aryan Kapoor", "email": "aryan@fitsphere.ai", "phone": "+91 98001 11001",
     "specialty": "Strength & Conditioning", "experience_years": 8, "rating": 4.9, "total_reviews": 142,
     "hourly_rate": 1200, "avatar_gradient": "linear-gradient(135deg,#3b82f6,#06b6d4)",
     "bio": "NSCA-certified strength coach with 8 years experience. Former national-level powerlifter.",
     "certifications": '["NSCA-CSCS","CPT","Precision Nutrition L1"]'},
    {"full_name": "Meena Sharma", "email": "meena@fitsphere.ai", "phone": "+91 98001 11002",
     "specialty": "Yoga & Wellness", "experience_years": 10, "rating": 4.8, "total_reviews": 198,
     "hourly_rate": 800, "avatar_gradient": "linear-gradient(135deg,#ec4899,#8b5cf6)",
     "bio": "RYT-500 certified yoga instructor and wellness coach. Specializes in therapeutic and prenatal yoga.",
     "certifications": '["RYT-500","Prenatal Yoga","Meditation Guide"]'},
    {"full_name": "Rohan Verma", "email": "rohan@fitsphere.ai", "phone": "+91 98001 11003",
     "specialty": "Sports Performance", "experience_years": 6, "rating": 4.7, "total_reviews": 87,
     "hourly_rate": 1000, "avatar_gradient": "linear-gradient(135deg,#f59e0b,#ef4444)",
     "bio": "Ex-professional cricketer turned performance coach. Expert in athletic conditioning and sports rehab.",
     "certifications": '["NASM-PES","ACE-CPT","Sports Nutrition"]'},
    {"full_name": "Pooja Nair", "email": "pooja@fitsphere.ai", "phone": "+91 98001 11004",
     "specialty": "Weight Loss Specialist", "experience_years": 9, "rating": 4.9, "total_reviews": 223,
     "hourly_rate": 900, "avatar_gradient": "linear-gradient(135deg,#10b981,#06b6d4)",
     "bio": "Transformed 200+ clients with sustainable weight loss programs. Published author of 'Smart Fat Loss'.",
     "certifications": '["ISSA-CPT","Precision Nutrition L2","Bariatric Exercise Specialist"]'},
    {"full_name": "Vikash Rao", "email": "vikash@fitsphere.ai", "phone": "+91 98001 11005",
     "specialty": "Bodybuilding & Powerlifting", "experience_years": 7, "rating": 4.6, "total_reviews": 95,
     "hourly_rate": 1100, "avatar_gradient": "linear-gradient(135deg,#8b5cf6,#3b82f6)",
     "bio": "3× State bodybuilding champion. Specializes in contest prep and advanced hypertrophy protocols.",
     "certifications": '["NPC Certified Judge","NASM-CPT","WNBF Pro Card"]'},
    {"full_name": "Sana Mirza", "email": "sana@fitsphere.ai", "phone": "+91 98001 11006",
     "specialty": "Functional Fitness & Mobility", "experience_years": 5, "rating": 4.8, "total_reviews": 167,
     "hourly_rate": 850, "avatar_gradient": "linear-gradient(135deg,#f97316,#eab308)",
     "bio": "FMS Level 2 certified. Expert in movement correction, injury prevention and functional training.",
     "certifications": '["FMS Level 2","NASM-CPT","TRX Suspension Training","Animal Flow"]'},
]
trainer_ids = []
for t in trainers_data:
    existing = db.query(models.Trainer).filter(models.Trainer.email == t["email"]).first()
    if not existing:
        trainer = models.Trainer(**t, joined_date=date.today() - timedelta(days=random.randint(365, 1800)))
        db.add(trainer)
        db.flush()
        trainer_ids.append(trainer.id)
    else:
        trainer_ids.append(existing.id)
db.commit()
print("  ✅ Trainers seeded")

# ── Members ───────────────────────────────────────────────────
members_data = [
    {"full_name": "Rahul Sharma", "email": "rahul.sharma@gmail.com", "phone": "+91 98765 43210",
     "gender": "Male", "blood_group": "B+", "avatar_color": "#f59e0b",
     "plan": "Elite", "goal": "Muscle Gain", "trainer_idx": 0},
    {"full_name": "Priya Mehta", "email": "priya.mehta@gmail.com", "phone": "+91 87654 32109",
     "gender": "Female", "blood_group": "A+", "avatar_color": "#8b5cf6",
     "plan": "Pro", "goal": "Weight Loss", "trainer_idx": 3},
    {"full_name": "Arjun Patel", "email": "arjun.patel@gmail.com", "phone": "+91 76543 21098",
     "gender": "Male", "blood_group": "O+", "avatar_color": "#10b981",
     "plan": "Elite", "goal": "Endurance", "trainer_idx": 2},
    {"full_name": "Sneha Kapoor", "email": "sneha.kapoor@gmail.com", "phone": "+91 65432 10987",
     "gender": "Female", "blood_group": "AB+", "avatar_color": "#f97316",
     "plan": "Pro", "goal": "Flexibility", "trainer_idx": 1},
    {"full_name": "Vikram Singh", "email": "vikram.singh@gmail.com", "phone": "+91 54321 09876",
     "gender": "Male", "blood_group": "B-", "avatar_color": "#ec4899",
     "plan": "Basic", "goal": "General Fitness", "trainer_idx": 5},
    {"full_name": "Riya Bose", "email": "riya.bose@gmail.com", "phone": "+91 43210 98765",
     "gender": "Female", "blood_group": "A-", "avatar_color": "#06b6d4",
     "plan": "Pro", "goal": "Weight Loss", "trainer_idx": 3, "status": "expired"},
    {"full_name": "Dev Khanna", "email": "dev.khanna@gmail.com", "phone": "+91 32109 87654",
     "gender": "Male", "blood_group": "O-", "avatar_color": "#34d399",
     "plan": "Basic", "goal": "Muscle Gain", "trainer_idx": 4},
    {"full_name": "Anjali Roy", "email": "anjali.roy@gmail.com", "phone": "+91 21098 76543",
     "gender": "Female", "blood_group": "B+", "avatar_color": "#ef4444",
     "plan": "Elite", "goal": "Endurance", "trainer_idx": 2, "status": "paused"},
    {"full_name": "Kiran Sharma", "email": "kiran.sharma@gmail.com", "phone": "+91 11098 76543",
     "gender": "Female", "blood_group": "A+", "avatar_color": "#a855f7",
     "plan": "Pro", "goal": "Weight Loss", "trainer_idx": 3},
    {"full_name": "Mohit Gupta", "email": "mohit.gupta@gmail.com", "phone": "+91 99001 22001",
     "gender": "Male", "blood_group": "O+", "avatar_color": "#3b82f6",
     "plan": "Elite", "goal": "Muscle Gain", "trainer_idx": 0},
    {"full_name": "Divya Krishnan", "email": "divya.krishnan@gmail.com", "phone": "+91 99001 22002",
     "gender": "Female", "blood_group": "AB-", "avatar_color": "#f43f5e",
     "plan": "Pro", "goal": "Flexibility", "trainer_idx": 1},
    {"full_name": "Aditya Joshi", "email": "aditya.joshi@gmail.com", "phone": "+91 99001 22003",
     "gender": "Male", "blood_group": "B+", "avatar_color": "#0ea5e9",
     "plan": "Basic", "goal": "General Fitness", "trainer_idx": 5},
]

member_ids = []
for m in members_data:
    existing = db.query(models.Member).filter(models.Member.email == m["email"]).first()
    if not existing:
        member = models.Member(
            full_name=m["full_name"], email=m["email"], phone=m["phone"],
            gender=m["gender"], blood_group=m.get("blood_group"),
            avatar_color=m["avatar_color"],
            date_of_birth=date(1990 + random.randint(0, 15), random.randint(1, 12), random.randint(1, 28)),
            created_at=datetime.utcnow() - timedelta(days=random.randint(30, 730))
        )
        db.add(member)
        db.flush()

        start = date.today() - timedelta(days=random.randint(30, 180))
        end = start + timedelta(days=30)
        status = m.get("status", "active")
        membership = models.Membership(
            member_id=member.id,
            plan_id=plan_map[m["plan"]],
            start_date=start,
            end_date=end if status == "expired" else date.today() + timedelta(days=random.randint(10, 90)),
            status=status,
            fitness_goal=m["goal"],
            assigned_trainer_id=trainer_ids[m["trainer_idx"]] if m["trainer_idx"] < len(trainer_ids) else None
        )
        db.add(membership)
        member_ids.append(member.id)
    else:
        member_ids.append(existing.id)

db.commit()
print(f"  ✅ Members seeded ({len(member_ids)})")

# ── Attendance Records (last 90 days) ─────────────────────────
workout_types = ["Strength", "Cardio", "HIIT", "Yoga", "CrossFit", "Boxing", "Cycling", "Swimming"]
if db.query(models.Attendance).count() < 100:
    for member_id in member_ids:
        for day_offset in range(90, 0, -1):
            if random.random() < 0.7:  # 70% attendance rate
                checkin_dt = datetime.utcnow() - timedelta(days=day_offset)
                checkin_dt = checkin_dt.replace(
                    hour=random.choice([6, 7, 8, 9, 17, 18, 19]),
                    minute=random.randint(0, 59)
                )
                duration = random.randint(45, 120)
                attendance = models.Attendance(
                    member_id=member_id,
                    check_in=checkin_dt,
                    check_out=checkin_dt + timedelta(minutes=duration),
                    duration_minutes=duration,
                    workout_type=random.choice(workout_types),
                    calories_burned=duration * random.randint(6, 10)
                )
                db.add(attendance)
    db.commit()
    print("  ✅ Attendance records seeded (90 days)")

# ── Sessions ──────────────────────────────────────────────────
session_templates = [
    ("Morning HIIT Power", "Group", 6, 60, 15),
    ("Yoga Flow & Breathwork", "Group", 8, 75, 12),
    ("Strength Circuit Training", "Group", 9, 60, 10),
    ("Personal Training — Elite", "Personal", 10, 60, 1),
    ("Spin & Cycle Class", "Group", 17, 45, 20),
    ("Boxing Fundamentals", "Group", 18, 60, 12),
    ("Functional Fitness Pro", "Group", 19, 60, 15),
    ("Late Night Cardio", "Group", 20, 45, 10),
]
if db.query(models.Session).count() < 30:
    for day_offset in range(-3, 14):
        for title, stype, hour, dur, cap in session_templates:
            if random.random() < 0.6:
                scheduled = datetime.utcnow().replace(hour=0, minute=0, second=0) + timedelta(days=day_offset, hours=hour)
                enrolled = random.randint(1, cap)
                session = models.Session(
                    trainer_id=random.choice(trainer_ids),
                    title=title, session_type=stype,
                    scheduled_at=scheduled,
                    duration_minutes=dur, max_capacity=cap,
                    current_enrolled=enrolled,
                    status="confirmed" if day_offset >= 0 else "completed",
                    price=0 if stype == "Group" else 1200
                )
                db.add(session)
    db.commit()
    print("  ✅ Sessions seeded")

# ── Payments ──────────────────────────────────────────────────
if db.query(models.Payment).count() < 50:
    methods = ["UPI", "Card", "Cash", "NetBanking", "Wallet"]
    statuses = ["paid", "paid", "paid", "paid", "pending", "failed"]
    for member_id in member_ids:
        for month_offset in range(12):
            paid_at = datetime.utcnow() - timedelta(days=30 * month_offset)
            plan_price = random.choice([999, 1999, 3499])
            payment = models.Payment(
                member_id=member_id,
                amount=plan_price,
                payment_method=random.choice(methods),
                transaction_ref=f"TXN-{uuid.uuid4().hex[:10].upper()}",
                status=random.choice(statuses),
                paid_at=paid_at + timedelta(days=random.randint(0, 5))
            )
            db.add(payment)
    db.commit()
    print("  ✅ Payments seeded (12 months)")

# ── Body Measurements ─────────────────────────────────────────
if db.query(models.BodyMeasurement).count() < 30:
    for member_id in member_ids[:6]:  # first 6 members
        weight = random.uniform(65, 90)
        height = random.uniform(160, 185)
        for month_offset in range(6):
            dt = date.today() - timedelta(days=30 * month_offset)
            bmi = round(weight / ((height / 100) ** 2), 1)
            measurement = models.BodyMeasurement(
                member_id=member_id, measured_at=dt,
                weight_kg=round(weight + (month_offset * 0.3 * (-1 if random.random() > 0.4 else 1)), 1),
                height_cm=round(height, 1),
                body_fat_pct=round(random.uniform(15, 28) - month_offset * 0.4, 1),
                muscle_mass_kg=round(random.uniform(45, 65) + month_offset * 0.2, 1),
                bmi=bmi,
                chest_cm=round(random.uniform(90, 105), 1),
                waist_cm=round(random.uniform(75, 95) - month_offset * 0.5, 1),
                hips_cm=round(random.uniform(90, 108), 1),
                arms_cm=round(random.uniform(30, 42) + month_offset * 0.1, 1),
            )
            db.add(measurement)
    db.commit()
    print("  ✅ Body measurements seeded")

# ── Meal Logs ─────────────────────────────────────────────────
meal_templates = [
    ("Breakfast", "Oatmeal with banana, protein shake, black coffee", 480, 42, 58, 12, 400),
    ("Snack", "Greek yogurt, almonds, apple", 280, 18, 32, 10, 300),
    ("Lunch", "Grilled chicken breast, brown rice, mixed salad", 620, 55, 65, 8, 500),
    ("Pre-workout", "Banana, peanut butter whole wheat toast", 340, 12, 52, 9, 250),
    ("Post-workout", "Whey protein shake, banana", 280, 38, 32, 2, 500),
    ("Dinner", "Salmon fillet, quinoa, steamed broccoli", 520, 46, 38, 18, 400),
]
if db.query(models.MealLog).count() < 100:
    for member_id in member_ids[:4]:
        for day_offset in range(7):
            for meal_type, food, cal, prot, carb, fat, water in meal_templates[:random.randint(3, 6)]:
                logged = datetime.utcnow() - timedelta(days=day_offset)
                db.add(models.MealLog(
                    member_id=member_id, meal_type=meal_type,
                    food_items=food, calories=cal, protein_g=prot,
                    carbs_g=carb, fats_g=fat, water_ml=water,
                    logged_at=logged
                ))
    db.commit()
    print("  ✅ Meal logs seeded")

# ── Reminders ─────────────────────────────────────────────────
if db.query(models.Reminder).count() < 5:
    reminder_data = [
        {"title": "Membership Renewal — Riya Bose", "description": "Elite plan expires in 3 days. Send renewal offer.",
         "reminder_type": "renewal", "channel": "whatsapp",
         "scheduled_at": datetime.utcnow() + timedelta(hours=2)},
        {"title": "Absence Alert — Anjali Roy", "description": "5 consecutive days without check-in detected.",
         "reminder_type": "absence", "channel": "sms",
         "scheduled_at": datetime.utcnow() + timedelta(hours=4)},
        {"title": "Monthly Body Assessment Due", "description": "Rahul Sharma's monthly progress review is pending.",
         "reminder_type": "custom", "channel": "app",
         "scheduled_at": datetime.utcnow() + timedelta(days=1)},
        {"title": "Bulk Renewal Campaign", "description": "87 members have expired memberships. Launch re-engagement campaign.",
         "reminder_type": "renewal", "channel": "email",
         "scheduled_at": datetime.utcnow() + timedelta(days=2)},
    ]
    for r in reminder_data:
        db.add(models.Reminder(**r, target_member_id=member_ids[0] if member_ids else None))
    db.commit()
    print("  ✅ Reminders seeded")

# ── AI Insights ───────────────────────────────────────────────
if db.query(models.AIInsight).count() < 4:
    insights = [
        {"insight_type": "peak_hours", "title": "Peak Traffic Detected: 6–8 AM", "severity": "info",
         "description": "6–8 AM sees 42% more footfall than other morning slots. Consider adding an additional trainer for this window.",
         "action_label": "Add Trainer Session"},
        {"insight_type": "revenue", "title": "₹87,000 Revenue Opportunity Identified", "severity": "success",
         "description": "87 expired members could generate ₹87,000+/month with a targeted re-engagement offer. Win-back rate typically 35–45%.",
         "action_label": "Launch Campaign"},
        {"insight_type": "attendance", "title": "HIIT Class Demand Surge (+34%)", "severity": "info",
         "description": "HIIT sessions are up 34% this week. Current capacity may be insufficient. Schedule 2 additional group HIIT sessions.",
         "action_label": "Add Sessions"},
        {"insight_type": "nutrition", "title": "63% of Members Below Protein Targets", "severity": "warning",
         "description": "Diet analysis shows 63% of tracked members are consistently below protein intake targets. This may limit their results.",
         "action_label": "Send Diet Reminder"},
        {"insight_type": "retention", "title": "Churn Risk: 23 Members Flagged", "severity": "critical",
         "description": "23 members haven't visited in 7+ days and their memberships expire in <15 days. Immediate outreach recommended.",
         "action_label": "Send Outreach"},
        {"insight_type": "equipment", "title": "Squat Rack Utilization: 94%", "severity": "warning",
         "description": "Squat rack usage is at 94% during peak hours (6–9 AM). Members report 15–20 min wait times. Consider adding equipment.",
         "action_label": "Review Equipment"},
    ]
    for ins in insights:
        db.add(models.AIInsight(**ins))
    db.commit()
    print("  ✅ AI Insights seeded")

db.close()
print("\n✅ Database seeded successfully!")
print("📊 Summary:")
print(f"  - Plans: {len(plans_data)}")
print(f"  - Trainers: {len(trainers_data)}")
print(f"  - Members: {len(members_data)}")
print(f"  - Attendance records: 90 days × members")
print(f"  - Sessions: ~2 weeks schedule")
print(f"  - Payments: 12 months history")
print("\n🚀 Run 'python main.py' to start the API server")
print("📖 API Docs: http://localhost:8000/docs")
