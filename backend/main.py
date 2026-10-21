"""
FitSphere AI Platform — FastAPI Backend
======================================
Author  : FitSphere Engineering
Version : 2.0.0
Stack   : Python 3.11 · FastAPI · SQLAlchemy · SQLite
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from app.database import engine, Base
from app.api.routes import (
    members, trainers, attendance,
    sessions, payments, measurements,
    workouts, diet, reminders, dashboard, ai_assistant
)

# ── Create all DB tables on startup ─────────────────────────────
Base.metadata.create_all(bind=engine)

# ── FastAPI app ──────────────────────────────────────────────────
app = FastAPI(
    title="FitSphere AI Platform API",
    description="""
## FitSphere — Intelligent Fitness Management System

A production-grade REST API powering the FitSphere platform.

### Features
- 🏋️ **Member Management** — Full CRUD with plan subscriptions
- 📍 **Smart Attendance** — Real-time check-in/out tracking
- 🤖 **AI Recommendations** — Personalized workout & diet plans
- 📊 **Analytics Dashboard** — Revenue, retention, performance KPIs
- 👨‍🏫 **Trainer Management** — Scheduling, ratings, specialties
- 🥗 **Diet Tracking** — Macro monitoring, meal logging
- 💰 **Revenue Intelligence** — Payments, forecasting, MRR
    """,
    version="2.0.0",
    contact={"name": "FitSphere Engineering", "email": "api@fitsphere.ai"},
    license_info={"name": "MIT"},
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ─────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Global exception handler ─────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}", "path": str(request.url)}
    )

# ── Routers ──────────────────────────────────────────────────────
app.include_router(dashboard.router,    prefix="/api/v1/dashboard",    tags=["Dashboard"])
app.include_router(members.router,      prefix="/api/v1/members",      tags=["Members"])
app.include_router(trainers.router,     prefix="/api/v1/trainers",     tags=["Trainers"])
app.include_router(attendance.router,   prefix="/api/v1/attendance",   tags=["Attendance"])
app.include_router(sessions.router,     prefix="/api/v1/sessions",     tags=["Sessions"])
app.include_router(payments.router,     prefix="/api/v1/payments",     tags=["Payments"])
app.include_router(measurements.router, prefix="/api/v1/measurements", tags=["Body Measurements"])
app.include_router(workouts.router,     prefix="/api/v1/workouts",     tags=["Workouts"])
app.include_router(diet.router,         prefix="/api/v1/diet",         tags=["Diet"])
app.include_router(reminders.router,    prefix="/api/v1/reminders",    tags=["Reminders"])
app.include_router(ai_assistant.router, prefix="/api/v1/ai",           tags=["AI Assistant"])

# ── Health check ─────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "service": "FitSphere API",
        "version": "2.0.0",
        "database": "connected"
    }

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to FitSphere AI Platform API",
        "docs": "/docs",
        "version": "2.0.0"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
