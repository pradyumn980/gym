from datetime import datetime, timedelta

def determine_level(history):
    """
    Decide user difficulty level based on workout consistency.
    """

    if not history:
        return "beginner"

    # Count workouts in last 7 days
    one_week_ago = datetime.now() - timedelta(days=7)
    recent_workouts = [
        h for h in history
        if "date" in h and datetime.fromisoformat(h["date"]) > one_week_ago
    ]

    if len(recent_workouts) >= 3:
        return "intermediate"

    return "beginner"
