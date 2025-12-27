export const getWorkoutRecommendation = async (history, level) => {
  const res = await fetch("http://127.0.0.1:5000/recommend-workout", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ history, level }),
  });

  if (!res.ok) {
    throw new Error("ML API failed");
  }

  return res.json();
};

export const getWeeklyPlan = async (history, preferences = {}) => {
  const res = await fetch("http://127.0.0.1:5000/generate-weekly-plan", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ history, preferences }),
  });

  if (!res.ok) {
    throw new Error("ML Generate Plan failed");
  }

  return res.json();
};
