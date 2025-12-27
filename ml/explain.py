def generate_reason(history, workout):
    """
    Explain why a workout was recommended
    """

    # Safely extract names
    recent = [
        h.get("name")
        for h in history[-2:]
        if h.get("name")
    ]

    if not recent:
        return (
            f"{workout} helps build a balanced routine "
            f"and keeps your training consistent."
        )

    muscles = ", ".join(recent)

    return (
        f"You recently trained **{muscles}**, "
        f"so **{workout}** helps balance muscle recovery and progress."
    )
