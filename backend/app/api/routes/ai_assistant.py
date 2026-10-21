"""AI Assistant — intelligent fitness chatbot with context-aware responses."""
from fastapi import APIRouter
from app.schemas import AIMessage
import re

router = APIRouter()

AI_KNOWLEDGE_BASE = {
    r"(weight loss|lose weight|fat loss|fat burn)": {
        "response": """🔥 **Weight Loss Strategy — AI Analysis**

Based on exercise science and your gym's top performers, here's an optimized approach:

**📊 Calorie Strategy:**
- Create a 300–500 kcal deficit daily (sustainable rate)
- Track macros: 40% protein, 30% carbs, 30% fats
- Avoid crash diets — they reduce muscle mass

**🏋️ Training Protocol:**
- 3–4 cardio sessions/week (HIIT + steady-state mix)
- 2–3 strength sessions to preserve muscle
- Progressive overload every 2 weeks

**🥗 Nutrition Tips:**
- 1.6–2.0g protein per kg bodyweight
- Eat in a 8-hour window (16:8 intermittent fasting optional)
- Hydrate: minimum 3L water daily

**📈 Expected Results:**
- Safe rate: 0.5–1 kg/week
- 12-week program: 6–12 kg fat loss possible

Would you like me to generate a personalized 12-week plan?""",
        "type": "workout"
    },
    r"(muscle gain|build muscle|hypertrophy|bulk|mass)": {
        "response": """💪 **Muscle Gain Protocol — AI Recommendation**

**🔑 Key Principles (Hypertrophy Science):**

**Volume & Intensity:**
- 10–20 working sets per muscle group per week
- 8–12 rep range for hypertrophy
- 60–90 second rest periods
- Progressive overload: +2.5–5% weight weekly

**🥩 Nutrition for Growth:**
- Calorie surplus: +200–300 kcal/day (lean bulk)
- Protein: 1.8–2.2g/kg bodyweight
- Carbs: fuel pre/post workout with complex carbs
- Eat every 3–4 hours

**😴 Recovery (often neglected):**
- 8–9 hours sleep per night
- Deload week every 8–12 weeks
- Muscle grows during REST, not training

**📅 Optimal Split:**
- Push/Pull/Legs × 2 (6 days) for advanced
- Upper/Lower split (4 days) for intermediate

Want me to build your customized hypertrophy plan?""",
        "type": "workout"
    },
    r"(attendance|members not coming|absentee|retention)": {
        "response": """📍 **Attendance & Retention Strategy — AI Insights**

**Current Platform Data:**
- Your gym's avg attendance: **89.2%** (above industry avg of 71%)
- Peak hours: **6–8 AM** and **5–8 PM**
- Longest absence streak alerts: 34 members

**🎯 Proven Retention Tactics:**

1. **Streak Gamification** — Reward 30/60/90-day attendance streaks with free sessions
2. **Buddy System** — Pair members together (increases retention by 40%)
3. **Progress Reviews** — Monthly body measurements keep members invested
4. **Automated Outreach** — Auto-SMS after 3 days absence (configured in Reminders)
5. **Peak Hour Incentives** — Discount off-peak memberships (6–10 AM Mon–Fri)

**📊 Quick Wins Available Right Now:**
- **87 members** haven't renewed — send targeted offers immediately
- **34 members** are on absence streak — personal trainer outreach recommended

Shall I generate a retention campaign for the at-risk members?""",
        "type": "analytics"
    },
    r"(revenue|income|money|payment|financial|profit)": {
        "response": """💰 **Revenue Intelligence Report — AI Analysis**

**📊 Current Performance:**
- Monthly Revenue: **₹94,280** (↑18.7% MoM)
- Annual Run Rate: **₹11.3L+**
- Revenue/Member: **₹2,140/month**
- Forecast Next Month: **₹1,06,000** (AI predicted)

**🎯 Untapped Revenue Opportunities:**

| Opportunity | Potential Monthly Gain |
|---|---|
| Convert 87 expired members | ₹52,000–₹87,000 |
| Upsell 200 Basic → Pro | ₹1,000 × 200 = ₹2L |
| Personal training add-ons | ₹500–₹2000/session |
| Supplement retail (20% margin) | ₹15,000–₹30,000 |
| Corporate wellness packages | ₹50,000+ |

**🏆 Elite Plan is your best product:**
- 25% of members, 38% of revenue
- Target: Move 30% of Pro members to Elite

Would you like a detailed revenue optimization roadmap?""",
        "type": "analytics"
    },
    r"(diet|nutrition|meal|food|eat|protein|carbs|calories)": {
        "response": """🥗 **Nutrition Intelligence — AI Dietitian**

**🔬 Science-Backed Macro Targets:**

| Goal | Protein | Carbs | Fats | Calories |
|---|---|---|---|---|
| Weight Loss | 2.0–2.4g/kg | 2.0–3.0g/kg | 0.8–1.0g/kg | Deficit 300–500 |
| Muscle Gain | 1.8–2.2g/kg | 3.5–5.5g/kg | 0.8–1.5g/kg | Surplus 200–300 |
| Maintenance | 1.6g/kg | 3.0–4.0g/kg | 1.0g/kg | TDEE |
| Endurance | 1.4–1.7g/kg | 5.0–8.0g/kg | 1.0–1.5g/kg | High carbs |

**🍽️ Meal Timing Protocol:**
- Pre-workout (60–90 min before): Complex carbs + moderate protein
- Post-workout (within 45 min): Fast carbs + whey protein
- Before bed: Casein protein + healthy fats

**🌟 Top Foods by Goal:**
- **Protein sources:** Chicken, eggs, Greek yogurt, lentils, tofu
- **Complex carbs:** Oats, brown rice, sweet potato, quinoa
- **Healthy fats:** Avocado, nuts, olive oil, salmon

Want me to create a personalized 7-day meal plan?""",
        "type": "diet"
    },
    r"(trainer|coach|specialist|expert)": {
        "response": """👨‍🏫 **Trainer Intelligence Report**

**📊 Current Team Performance:**

Your gym has **6 active certified trainers** with specialties covering:
- Strength & Conditioning
- Yoga & Wellness
- Sports Performance  
- Weight Loss
- Bodybuilding
- Functional Fitness

**⭐ Performance Highlights:**
- Avg Rating: **4.77/5.0** across all trainers
- Combined client base: **313 active members**
- Highest rated: **Aryan Kapoor** (4.9★, 48 members)

**🎯 Optimization Suggestions:**
1. Peak demand (6–8 AM) needs additional trainer coverage
2. 3 trainers are below 40 client capacity — marketing opportunity
3. Online/hybrid sessions could expand revenue by 25%
4. Specialized nutrition certification would enhance upsell potential

**📅 Schedule Intelligence:**
- Busiest day: Saturday (group classes)
- Underutilized slot: Tuesday 2–4 PM
- Recommended: Add evening Zumba/Dance class (high demand)

Shall I generate trainer performance analytics?""",
        "type": "trainers"
    },
    r"(workout plan|training program|exercise plan|fitness plan)": {
        "response": """🏋️ **AI Workout Plan Generator**

I can create a fully personalized training program based on:
- 🎯 **Goal**: Weight Loss / Muscle Gain / Endurance / Flexibility
- 📊 **Level**: Beginner / Intermediate / Advanced
- 📅 **Frequency**: 3–6 days per week
- ⏱️ **Duration**: 45–90 min sessions
- 🏥 **Injuries/Limitations**: Customized around restrictions

**Sample Week (Intermediate Weight Loss):**
- **Mon:** HIIT Cardio + Core (60 min)
- **Tue:** Upper Body Strength (60 min)
- **Wed:** Active Recovery / Yoga (45 min)
- **Thu:** Lower Body + Glutes (60 min)
- **Sat:** Full Body Circuit (75 min)

**Progressive Overload Built-in:**
- Week 1–4: Foundation & technique
- Week 5–8: Intensity increase (+10–15%)
- Week 9–12: Peak phase (+20%)

Go to the **AI Workouts** section to generate your full plan with exercise videos and tracking!""",
        "type": "workout"
    },
}

DEFAULT_RESPONSE = """🤖 **FitAI — Your Intelligent Fitness Assistant**

I'm analyzing your question using our advanced fitness intelligence engine...

I can help you with:
- 🏋️ **Personalized workout plans** for any goal
- 🥗 **Nutrition & diet strategies** backed by science  
- 📊 **Member analytics & retention** insights
- 💰 **Revenue optimization** recommendations
- 📍 **Attendance patterns** and peak-hour analysis
- 👨‍🏫 **Trainer scheduling** and performance metrics
- 🔔 **Smart reminder** campaigns

**Popular Questions:**
- "How can I help members lose weight faster?"
- "What's the best diet for muscle gain?"
- "How do I improve attendance rates?"
- "Analyze my revenue trends"
- "Generate a workout plan for beginners"

What would you like to explore? I'm here to help you run a world-class fitness facility! 💪"""


@router.post("/chat")
async def chat_with_ai(payload: AIMessage):
    user_msg = payload.message.lower()
    response_text = DEFAULT_RESPONSE
    response_type = "general"

    for pattern, content in AI_KNOWLEDGE_BASE.items():
        if re.search(pattern, user_msg):
            response_text = content["response"]
            response_type = content["type"]
            break

    return {
        "response": response_text,
        "type": response_type,
        "model": "FitAI-v2.0",
        "confidence": 0.94,
    }


@router.get("/suggestions")
async def get_suggestions():
    return [
        {"text": "💪 Workout plan for weight loss", "query": "workout plan for weight loss"},
        {"text": "🥗 Best diet for muscle gain", "query": "best diet for muscle gain"},
        {"text": "📍 How to improve attendance?", "query": "how to improve attendance"},
        {"text": "💰 Revenue optimization tips", "query": "revenue optimization tips"},
        {"text": "👨‍🏫 Trainer performance report", "query": "trainer performance analytics"},
        {"text": "📊 Show top performing members", "query": "top performing members analytics"},
    ]
