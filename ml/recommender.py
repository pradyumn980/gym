import random
from fatigue import check_fatigue
from explain import generate_reason
from progression import determine_level

# -------------------------
# Exercise → Muscle mapping
# -------------------------
MUSCLE_MAP = {
    "Push-ups": "Chest",
    "Bench Press": "Chest",
    "Pull-ups": "Back",
    "Deadlifts": "Back",
    "Squats": "Legs",
    "Lunges": "Legs",
    "Cycling": "Cardio",
    "Running": "Cardio",
    "Plank": "Core",
    "Crunches": "Core",
}

# -------------------------
# Available workout options
# -------------------------
WORKOUTS = [
    {"name": "Chest", "type": "strength"},
    {"name": "Back", "type": "strength"},
    {"name": "Legs", "type": "strength"},
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
