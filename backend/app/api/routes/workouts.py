"""AI Workout recommendation routes."""
from fastapi import APIRouter, HTTPException
from typing import Optional

router = APIRouter()

WORKOUT_LIBRARY = {
    "Weight Loss": {
        "Beginner": [
            {"day": "Monday", "type": "Cardio + Core", "color": "#ef4444",
             "exercises": [{"name": "Treadmill Walk/Run", "sets": "30 min", "muscle": "Cardio"}, {"name": "Plank", "sets": "3×45s", "muscle": "Core"}, {"name": "Mountain Climbers", "sets": "3×15", "muscle": "Core"}, {"name": "Jumping Jacks", "sets": "3×30", "muscle": "Full Body"}]},
            {"day": "Wednesday", "type": "Lower Body", "color": "#8b5cf6",
             "exercises": [{"name": "Bodyweight Squats", "sets": "3×15", "muscle": "Quads"}, {"name": "Lunges", "sets": "3×12 each", "muscle": "Glutes"}, {"name": "Glute Bridges", "sets": "3×15", "muscle": "Glutes"}, {"name": "Calf Raises", "sets": "3×20", "muscle": "Calves"}]},
            {"day": "Friday", "type": "Upper Body + HIIT", "color": "#f97316",
             "exercises": [{"name": "Push-ups", "sets": "3×10", "muscle": "Chest"}, {"name": "Dumbbell Row", "sets": "3×12", "muscle": "Back"}, {"name": "Burpees", "sets": "4×10", "muscle": "Full Body"}, {"name": "Tricep Dips", "sets": "3×12", "muscle": "Triceps"}]},
        ],
        "Intermediate": [
            {"day": "Monday", "type": "HIIT Cardio", "color": "#ef4444",
             "exercises": [{"name": "Sprint Intervals", "sets": "8×30s", "muscle": "Cardio"}, {"name": "Box Jumps", "sets": "4×12", "muscle": "Full Body"}, {"name": "Burpees", "sets": "4×15", "muscle": "Full Body"}, {"name": "Jump Rope", "sets": "5×2min", "muscle": "Cardio"}]},
            {"day": "Tuesday", "type": "Upper Strength", "color": "#3b82f6",
             "exercises": [{"name": "Bench Press", "sets": "4×10", "muscle": "Chest"}, {"name": "Pull-ups", "sets": "4×8", "muscle": "Back"}, {"name": "Shoulder Press", "sets": "3×12", "muscle": "Shoulders"}, {"name": "Bicep Curls", "sets": "3×12", "muscle": "Biceps"}]},
            {"day": "Thursday", "type": "Lower Strength", "color": "#8b5cf6",
             "exercises": [{"name": "Squats", "sets": "4×12", "muscle": "Quads"}, {"name": "Romanian Deadlift", "sets": "4×10", "muscle": "Hamstrings"}, {"name": "Leg Press", "sets": "4×12", "muscle": "Quads"}, {"name": "Walking Lunges", "sets": "3×20", "muscle": "Glutes"}]},
            {"day": "Saturday", "type": "Cardio Endurance", "color": "#10b981",
             "exercises": [{"name": "Cycling", "sets": "45 min", "muscle": "Cardio"}, {"name": "Battle Ropes", "sets": "5×30s", "muscle": "Upper Body"}, {"name": "Plank Circuit", "sets": "4×60s", "muscle": "Core"}, {"name": "Stair Climber", "sets": "20 min", "muscle": "Cardio"}]},
        ],
        "Advanced": [
            {"day": "Monday", "type": "Power Cardio", "color": "#ef4444",
             "exercises": [{"name": "Kettlebell Swings", "sets": "5×20", "muscle": "Full Body"}, {"name": "Barbell Thrusters", "sets": "5×10", "muscle": "Full Body"}, {"name": "Assault Bike", "sets": "10×20s", "muscle": "Cardio"}, {"name": "Sled Push", "sets": "6×20m", "muscle": "Legs/Cardio"}]},
            {"day": "Tuesday", "type": "Upper Power", "color": "#3b82f6",
             "exercises": [{"name": "Weighted Pull-ups", "sets": "5×6", "muscle": "Back"}, {"name": "Incline Bench Press", "sets": "5×8", "muscle": "Chest"}, {"name": "Arnold Press", "sets": "4×10", "muscle": "Shoulders"}, {"name": "Face Pulls", "sets": "4×15", "muscle": "Rear Delts"}]},
            {"day": "Wednesday", "type": "Lower Power", "color": "#8b5cf6",
             "exercises": [{"name": "Back Squat", "sets": "5×5", "muscle": "Quads"}, {"name": "Deadlift", "sets": "5×4", "muscle": "Posterior Chain"}, {"name": "Bulgarian Split Squat", "sets": "4×8", "muscle": "Glutes"}, {"name": "Nordic Curl", "sets": "4×6", "muscle": "Hamstrings"}]},
            {"day": "Thursday", "type": "Metabolic Conditioning", "color": "#f97316",
             "exercises": [{"name": "Clean & Press", "sets": "5×8", "muscle": "Full Body"}, {"name": "Box Jump + Broad Jump", "sets": "5×5", "muscle": "Plyometrics"}, {"name": "Toes-to-Bar", "sets": "4×10", "muscle": "Core"}, {"name": "Farmer's Walk", "sets": "6×30m", "muscle": "Full Body"}]},
            {"day": "Saturday", "type": "Endurance + Recovery", "color": "#10b981",
             "exercises": [{"name": "Long Run/Swim", "sets": "60 min", "muscle": "Cardio"}, {"name": "Mobility Flow", "sets": "20 min", "muscle": "Flexibility"}, {"name": "Foam Rolling", "sets": "15 min", "muscle": "Recovery"}, {"name": "Cold Exposure", "sets": "5 min", "muscle": "Recovery"}]},
        ]
    },
    "Muscle Gain": {
        "Intermediate": [
            {"day": "Monday", "type": "Chest & Triceps", "color": "#3b82f6",
             "exercises": [{"name": "Bench Press", "sets": "5×5", "muscle": "Chest"}, {"name": "Incline DB Press", "sets": "4×8", "muscle": "Upper Chest"}, {"name": "Cable Flyes", "sets": "3×12", "muscle": "Chest"}, {"name": "Tricep Pushdown", "sets": "4×12", "muscle": "Triceps"}]},
            {"day": "Tuesday", "type": "Back & Biceps", "color": "#10b981",
             "exercises": [{"name": "Deadlift", "sets": "5×5", "muscle": "Full Back"}, {"name": "Barbell Row", "sets": "4×8", "muscle": "Mid Back"}, {"name": "Lat Pulldown", "sets": "4×10", "muscle": "Lats"}, {"name": "Hammer Curls", "sets": "3×12", "muscle": "Biceps"}]},
            {"day": "Thursday", "type": "Shoulders & Arms", "color": "#f59e0b",
             "exercises": [{"name": "Military Press", "sets": "5×5", "muscle": "Shoulders"}, {"name": "Lateral Raises", "sets": "4×15", "muscle": "Side Delts"}, {"name": "EZ Bar Curl", "sets": "4×10", "muscle": "Biceps"}, {"name": "Skull Crushers", "sets": "4×10", "muscle": "Triceps"}]},
            {"day": "Friday", "type": "Legs & Glutes", "color": "#8b5cf6",
             "exercises": [{"name": "Back Squat", "sets": "5×5", "muscle": "Quads"}, {"name": "Leg Press", "sets": "4×12", "muscle": "Quads"}, {"name": "Hip Thrust", "sets": "4×12", "muscle": "Glutes"}, {"name": "Leg Curl", "sets": "4×12", "muscle": "Hamstrings"}]},
        ]
    }
}

@router.get("/plan")
def get_workout_plan(
    goal: str = "Weight Loss",
    level: str = "Intermediate",
    days_per_week: int = 4
):
    goal_plans = WORKOUT_LIBRARY.get(goal, WORKOUT_LIBRARY["Weight Loss"])
    level_plan = goal_plans.get(level, list(goal_plans.values())[0])
    return {
        "goal": goal, "level": level,
        "days_per_week": min(days_per_week, len(level_plan)),
        "plan": level_plan[:days_per_week],
        "ai_generated": True,
        "notes": f"This {level.lower()} plan is optimized for {goal.lower()} with {days_per_week} training days per week. Progressive overload every 2 weeks is recommended."
    }

@router.get("/exercises")
def get_exercise_library(muscle_group: Optional[str] = None):
    library = {
        "Chest": ["Bench Press", "Incline DB Press", "Cable Flyes", "Push-ups", "Dips"],
        "Back": ["Deadlift", "Pull-ups", "Barbell Row", "Lat Pulldown", "Seated Cable Row"],
        "Legs": ["Squat", "Leg Press", "Lunges", "Romanian Deadlift", "Leg Curl"],
        "Shoulders": ["Military Press", "Lateral Raises", "Face Pulls", "Arnold Press"],
        "Arms": ["Barbell Curl", "Tricep Pushdown", "Hammer Curls", "Skull Crushers"],
        "Core": ["Plank", "Hanging Leg Raises", "Russian Twists", "Ab Wheel"],
        "Cardio": ["Treadmill", "Cycling", "Rowing Machine", "Jump Rope", "HIIT"]
    }
    if muscle_group:
        return {muscle_group: library.get(muscle_group, [])}
    return library
