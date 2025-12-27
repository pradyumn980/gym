import random
from fatigue import check_fatigue
from explain import generate_reason
from progression import determine_level

# -------------------------
# Exercise → Muscle mapping
# -------------------------
MUSCLE_MAP = {
    # Chest
    "Push-ups": "Chest",
    "Bench Press": "Chest",
    "Incline Bench": "Chest",
    "Dips": "Chest",
    "Cable Flys": "Chest",
    "Chest Press": "Chest",

    # Back
    "Pull-ups": "Back",
    "Deadlifts": "Back",
    "Lat Pulldowns": "Back",
    "Seated Rows": "Back",
    "T-Bar Row": "Back",
    "Face Pulls": "Back",

    # Legs
    "Squats": "Legs",
    "Lunges": "Legs",
    "Leg Press": "Legs",
    "Romanian Deadlifts": "Legs",
    "Leg Extensions": "Legs",
    "Hamstring Curls": "Legs",
    "Calf Raises": "Legs",

    # Shoulders
    "Overhead Press": "Shoulders",
    "Lateral Raises": "Shoulders",
    "Front Raises": "Shoulders",
    "Arnold Press": "Shoulders",

    # Arms
    "Bicep Curls": "Arms",
    "Tricep Extensions": "Arms",
    "Hammer Curls": "Arms",
    "Skull Crushers": "Arms",

    # Core
    "Plank": "Core",
    "Crunches": "Core",
    "Leg Raises": "Core",
    "Russian Twists": "Core",
    "Bicycle Crunches": "Core",
    "Ab Wheel": "Core",

    # Cardio
    "Cycling": "Cardio",
    "Running": "Cardio",
    "Jump Rope": "Cardio",
    "Rowing Machine": "Cardio",
    "HIIT Sprints": "Cardio",
    "Elliptical": "Cardio",
}

# -------------------------
# Available workout options
# -------------------------
WORKOUTS = [
    {"name": "Chest", "type": "strength"},
    {"name": "Back", "type": "strength"},
    {"name": "Legs", "type": "strength"},
    {"name": "Shoulders", "type": "strength"},
    {"name": "Arms", "type": "strength"},
    {"name": "Core", "type": "strength"},
    {"name": "Cardio", "type": "cardio"},
    {"name": "Full Body", "type": "strength"},
    {"name": "Active Recovery", "type": "recovery"},
]

def normalize_history(history):
    """
    Converts exercise names into muscle groups
    """
    normalized = []
    for w in history:
        name = w.get("name")
        muscle = MUSCLE_MAP.get(name, name)
        normalized.append({"name": muscle})
    return normalized


def recommend_workout(history):
    """
    Main AI workout recommender
    """

    # 0️⃣ Normalize history (CRITICAL FIX)
    normalized_history = normalize_history(history)

    # 1️⃣ Determine user level automatically
    level = determine_level(normalized_history)

    # 2️⃣ Fatigue detection (highest priority)
    if check_fatigue(normalized_history):
        return {
            "workout": "Active Recovery",
            "duration": 20,
            "intensity": "low",
            "reason": (
                "You have recently trained the same muscle groups multiple times. "
                "An active recovery session will reduce fatigue and prevent injury."
            ),
        }

    # 3️⃣ Avoid recently trained muscle groups
    recent = normalized_history[-2:] if len(normalized_history) >= 2 else normalized_history
    recent_names = [w["name"] for w in recent]

    possible = [
        w for w in WORKOUTS
        if w["name"] not in recent_names and w["type"] != "recovery"
    ]

    # 4️⃣ Safety fallback (prevents random.choice crash)
    if not possible:
        possible = [w for w in WORKOUTS if w["type"] != "recovery"]

    workout = random.choice(possible)

    # 5️⃣ Duration based on progression level
    if level == "beginner":
        duration = 30
    elif level == "intermediate":
        duration = 45
    else:
        duration = 60

    # 6️⃣ Explainable AI output
    reason = generate_reason(normalized_history, workout["name"])

    return {
        "workout": workout["name"],
        "duration": duration,
        "intensity": level,
        "reason": reason,
    }
def generate_weekly_plan(history, preferences=None):
    """
    Generates a full weekly schedule based on user level and preferences.
    preferences: { 'goal': 'build_muscle'|'lose_weight'|..., 'days_per_week': 3|4|5|6 }
    """
    normalized_history = normalize_history(history)
    level = determine_level(normalized_history)
    
    # Defaults
    target_days = 3
    goal = "build_muscle"
    
    if preferences:
        target_days = int(preferences.get("days_per_week", 3))
        goal = preferences.get("goal", "build_muscle")
    elif level == "intermediate":
        target_days = 4
    elif level == "advanced":
        target_days = 6

    # Adjust parameters based on goal
    reps = 10
    rest = 60
    if goal == "lose_weight":
        reps = 15
        rest = 30
    elif goal == "strength":
        reps = 5
        rest = 120
    elif goal == "endurance":
        reps = 20
        rest = 30
    
    # Helper to get exercises
    def get_exercises(target_muscles, count=2):
        selected = []
        for muscle in target_muscles:
            options = [name for name, group in MUSCLE_MAP.items() if group == muscle]
            if options:
                picks = random.sample(options, min(len(options), count))
                for pick in picks:
                    selected.append({
                        "id": random.randint(10000, 99999),
                        "name": pick,
                        "sets": 3, # Standard
                        "reps": reps,
                        "rest": rest
                    })
        return selected

    schedule = {}
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    # Define Splits
    if target_days <= 3:
        # Full Body 3x
        active_days = ['Mon', 'Wed', 'Fri']
        for day in days:
            if day in active_days:
                schedule[day] = { "muscle": "Full Body", "exercises": get_exercises(["Chest", "Back", "Legs", "Shoulders", "Core"], 1) }
            else:
                schedule[day] = { "muscle": "Rest", "exercises": [] }

    elif target_days == 4:
        # Upper / Lower
        active_days = ['Mon', 'Tue', 'Thu', 'Fri']
        for day in days:
            if day in ['Mon', 'Thu']:
                schedule[day] = { "muscle": "Upper Body", "exercises": get_exercises(["Chest", "Back", "Shoulders", "Arms"], 1) + get_exercises(["Chest"], 1) }
            elif day in ['Tue', 'Fri']:
                 schedule[day] = { "muscle": "Lower Body", "exercises": get_exercises(["Legs"], 2) + get_exercises(["Core"], 1) }
            else:
                 schedule[day] = { "muscle": "Rest", "exercises": [] }

    elif target_days == 5:
        # PPL + Upper + Lower (Hybrid)
        # Mon: Push, Tue: Pull, Wed: Legs, Thu: Rest, Fri: Upper, Sat: Lower, Sun: Rest
        schedule['Mon'] = { "muscle": "Push", "exercises": get_exercises(["Chest"], 2) + get_exercises(["Shoulders"], 1) + get_exercises(["Arms"], 1) }
        schedule['Tue'] = { "muscle": "Pull", "exercises": get_exercises(["Back"], 2) + get_exercises(["Arms"], 1) }
        schedule['Wed'] = { "muscle": "Legs", "exercises": get_exercises(["Legs"], 3) }
        schedule['Thu'] = { "muscle": "Rest", "exercises": [] }
        schedule['Fri'] = { "muscle": "Upper Body", "exercises": get_exercises(["Chest", "Back", "Shoulders"], 1) }
        schedule['Sat'] = { "muscle": "Lower Body", "exercises": get_exercises(["Legs", "Core"], 2) }
        schedule['Sun'] = { "muscle": "Rest", "exercises": [] }

    elif target_days >= 6:
        # PPL x2
        # Mon: Push, Tue: Pull, Wed: Legs, Thu: Push, Fri: Pull, Sat: Legs, Sun: Rest
        rotation = ["Push", "Pull", "Legs", "Push", "Pull", "Legs", "Rest"]
        for i, day in enumerate(days):
            focus = rotation[i]
            if focus == "Push":
                schedule[day] = { "muscle": "Push", "exercises": get_exercises(["Chest"], 2) + get_exercises(["Shoulders"], 1) + get_exercises(["Arms"], 1) }
            elif focus == "Pull":
                schedule[day] = { "muscle": "Pull", "exercises": get_exercises(["Back"], 2) + get_exercises(["Arms"], 1) }
            elif focus == "Legs":
                schedule[day] = { "muscle": "Legs", "exercises": get_exercises(["Legs"], 3) + get_exercises(["Core"], 1) }
            else:
                schedule[day] = { "muscle": "Rest", "exercises": [] }
                
    return {"level": level, "split": f"{target_days}-Day Split", "schedule": schedule}
