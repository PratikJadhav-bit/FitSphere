-- ================================================================
-- FitSphere AI Platform — Database Schema
-- Designed for SQLite (compatible with PostgreSQL)
-- Author: FitSphere Engineering Team
-- Version: 2.0.0
-- ================================================================

PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

-- ── Members ────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS members (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name       TEXT    NOT NULL,
    email           TEXT    UNIQUE NOT NULL,
    phone           TEXT    NOT NULL,
    gender          TEXT    CHECK(gender IN ('Male','Female','Other')),
    date_of_birth   DATE,
    blood_group     TEXT,
    address         TEXT,
    emergency_contact TEXT,
    avatar_color    TEXT    DEFAULT '#3b82f6',
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ── Membership Plans ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS plans (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT    NOT NULL UNIQUE,       -- Basic, Pro, Elite
    price_monthly   REAL    NOT NULL,
    price_quarterly REAL,
    price_annual    REAL,
    features        TEXT,                          -- JSON array
    max_sessions    INTEGER DEFAULT -1,            -- -1 = unlimited
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ── Memberships (Member ↔ Plan subscription) ──────────────────
CREATE TABLE IF NOT EXISTS memberships (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id       INTEGER NOT NULL REFERENCES members(id) ON DELETE CASCADE,
    plan_id         INTEGER NOT NULL REFERENCES plans(id),
    start_date      DATE    NOT NULL,
    end_date        DATE    NOT NULL,
    status          TEXT    DEFAULT 'active' CHECK(status IN ('active','expired','paused','cancelled')),
    fitness_goal    TEXT    CHECK(fitness_goal IN ('Weight Loss','Muscle Gain','Endurance','Flexibility','General Fitness')),
    assigned_trainer_id INTEGER REFERENCES trainers(id),
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ── Trainers ───────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS trainers (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name       TEXT    NOT NULL,
    email           TEXT    UNIQUE NOT NULL,
    phone           TEXT,
    specialty       TEXT    NOT NULL,
    experience_years INTEGER DEFAULT 1,
    bio             TEXT,
    certifications  TEXT,                          -- JSON array
    rating          REAL    DEFAULT 5.0 CHECK(rating BETWEEN 1 AND 5),
    total_reviews   INTEGER DEFAULT 0,
    hourly_rate     REAL    DEFAULT 500,
    avatar_gradient TEXT    DEFAULT 'linear-gradient(135deg,#3b82f6,#06b6d4)',
    is_active       INTEGER DEFAULT 1,
    joined_date     DATE    DEFAULT CURRENT_DATE,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ── Attendance ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS attendance (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id       INTEGER NOT NULL REFERENCES members(id) ON DELETE CASCADE,
    check_in        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    check_out       DATETIME,
    duration_minutes INTEGER,
    workout_type    TEXT,
    calories_burned INTEGER,
    notes           TEXT,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ── Sessions ───────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS sessions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    trainer_id      INTEGER NOT NULL REFERENCES trainers(id),
    title           TEXT    NOT NULL,
    session_type    TEXT    CHECK(session_type IN ('Personal','Group','Online')),
    scheduled_at    DATETIME NOT NULL,
    duration_minutes INTEGER DEFAULT 60,
    max_capacity    INTEGER DEFAULT 1,
    current_enrolled INTEGER DEFAULT 0,
    status          TEXT    DEFAULT 'scheduled' CHECK(status IN ('scheduled','confirmed','in_progress','completed','cancelled')),
    location        TEXT    DEFAULT 'Main Gym Floor',
    price           REAL    DEFAULT 0,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ── Session Bookings ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS session_bookings (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id      INTEGER NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    member_id       INTEGER NOT NULL REFERENCES members(id) ON DELETE CASCADE,
    booked_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
    status          TEXT    DEFAULT 'confirmed' CHECK(status IN ('confirmed','cancelled','attended','no_show')),
    UNIQUE(session_id, member_id)
);

-- ── Body Measurements ──────────────────────────────────────────
CREATE TABLE IF NOT EXISTS body_measurements (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id       INTEGER NOT NULL REFERENCES members(id) ON DELETE CASCADE,
    measured_at     DATE    NOT NULL DEFAULT CURRENT_DATE,
    weight_kg       REAL,
    height_cm       REAL,
    body_fat_pct    REAL,
    muscle_mass_kg  REAL,
    bmi             REAL,
    chest_cm        REAL,
    waist_cm        REAL,
    hips_cm         REAL,
    arms_cm         REAL,
    thighs_cm       REAL,
    notes           TEXT,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ── Workout Plans ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS workout_plans (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT    NOT NULL,
    goal            TEXT    NOT NULL,
    level           TEXT    CHECK(level IN ('Beginner','Intermediate','Advanced')),
    days_per_week   INTEGER DEFAULT 4,
    duration_weeks  INTEGER DEFAULT 12,
    description     TEXT,
    created_by      INTEGER REFERENCES trainers(id),
    is_ai_generated INTEGER DEFAULT 0,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ── Member Workout Assignments ─────────────────────────────────
CREATE TABLE IF NOT EXISTS member_workout_assignments (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id       INTEGER NOT NULL REFERENCES members(id) ON DELETE CASCADE,
    plan_id         INTEGER NOT NULL REFERENCES workout_plans(id),
    assigned_at     DATE    DEFAULT CURRENT_DATE,
    is_active       INTEGER DEFAULT 1
);

-- ── Meal Logs ──────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS meal_logs (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id       INTEGER NOT NULL REFERENCES members(id) ON DELETE CASCADE,
    meal_type       TEXT    CHECK(meal_type IN ('Breakfast','Lunch','Dinner','Snack','Pre-workout','Post-workout')),
    food_items      TEXT    NOT NULL,
    calories        INTEGER,
    protein_g       REAL,
    carbs_g         REAL,
    fats_g          REAL,
    water_ml        INTEGER DEFAULT 0,
    logged_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
    notes           TEXT
);

-- ── Payments ───────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS payments (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id       INTEGER NOT NULL REFERENCES members(id) ON DELETE CASCADE,
    membership_id   INTEGER REFERENCES memberships(id),
    amount          REAL    NOT NULL,
    payment_method  TEXT    CHECK(payment_method IN ('Cash','UPI','Card','NetBanking','Wallet')),
    transaction_ref TEXT    UNIQUE,
    status          TEXT    DEFAULT 'paid' CHECK(status IN ('paid','pending','failed','refunded')),
    paid_at         DATETIME DEFAULT CURRENT_TIMESTAMP,
    notes           TEXT
);

-- ── Reminders ──────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS reminders (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    title           TEXT    NOT NULL,
    description     TEXT,
    reminder_type   TEXT    CHECK(reminder_type IN ('renewal','absence','diet','session','birthday','custom')),
    target_member_id INTEGER REFERENCES members(id),
    scheduled_at    DATETIME NOT NULL,
    is_sent         INTEGER DEFAULT 0,
    is_active       INTEGER DEFAULT 1,
    channel         TEXT    DEFAULT 'app' CHECK(channel IN ('app','sms','email','whatsapp')),
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ── AI Insights ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ai_insights (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    insight_type    TEXT    NOT NULL,
    title           TEXT    NOT NULL,
    description     TEXT    NOT NULL,
    severity        TEXT    DEFAULT 'info' CHECK(severity IN ('info','warning','success','critical')),
    action_label    TEXT,
    is_dismissed    INTEGER DEFAULT 0,
    generated_at    DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ── Indexes for performance ────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_attendance_member    ON attendance(member_id);
CREATE INDEX IF NOT EXISTS idx_attendance_checkin   ON attendance(check_in);
CREATE INDEX IF NOT EXISTS idx_memberships_member   ON memberships(member_id);
CREATE INDEX IF NOT EXISTS idx_memberships_status   ON memberships(status);
CREATE INDEX IF NOT EXISTS idx_payments_member      ON payments(member_id);
CREATE INDEX IF NOT EXISTS idx_payments_status      ON payments(status);
CREATE INDEX IF NOT EXISTS idx_sessions_trainer     ON sessions(trainer_id);
CREATE INDEX IF NOT EXISTS idx_sessions_scheduled   ON sessions(scheduled_at);
CREATE INDEX IF NOT EXISTS idx_meal_logs_member     ON meal_logs(member_id);
CREATE INDEX IF NOT EXISTS idx_body_measurements_m  ON body_measurements(member_id);
CREATE INDEX IF NOT EXISTS idx_reminders_scheduled  ON reminders(scheduled_at);
