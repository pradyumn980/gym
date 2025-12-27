def check_fatigue(history):
    if len(history) < 3:
        return False

    recent = [h["name"] for h in history[-3:]]
    return len(set(recent)) == 1
