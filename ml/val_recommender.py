from recommender import normalize_history, recommend_workout, MUSCLE_MAP

print("--- Test 1: Exercise Mapping ---")
new_exercise = "Overhead Press"
muscle = MUSCLE_MAP.get(new_exercise)
print(f"Exercise: {new_exercise} -> Muscle: {muscle}")

if muscle == "Shoulders":
    print("✅ SUCCESS: Mapping correct.")
else:
    print("❌ FAILURE: Mapping incorrect.")

print("\n--- Test 2: Recommendation Generation ---")
# Force a recommendation scenario where shoulders is valid
# History: Legs, Back. Shoulders is not in history, so it's a candidate.
history = [{"name": "Squats"}, {"name": "Pull-ups"}] 
rec = recommend_workout(history)
print(f"Recommendation: {rec['workout']}")

if rec['workout'] in ["Chest", "Shoulders", "Arms", "Core", "Cardio", "Full Body"]:
     print("✅ SUCCESS: Valid recommendation generated.")
else:
     print(f"❌ FAILURE: Unexpected recommendation: {rec['workout']}")

print("\n--- Test 3: History Normalization with New Exercises ---")
complex_history = [{"name": "Overhead Press"}, {"name": "Leg Press"}, {"name": "Plank"}]
normalized = normalize_history(complex_history)
print(f"Input: {complex_history}")
print(f"Normalized: {normalized}")

expected = [{"name": "Shoulders"}, {"name": "Legs"}, {"name": "Core"}]
if normalized == expected:
    print("✅ SUCCESS: Normalization correct.")
else:
    print("❌ FAILURE: Normalization incorrect.")
