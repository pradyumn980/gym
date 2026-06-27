const ML_API_BASE =
  window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
    ? "http://localhost:5000"
    : "https://gym-ybl2.onrender.com";

export const getWorkoutRecommendation = async (history, level) => {
  const res = await fetch(`${ML_API_BASE}/recommend-workout`, {
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
  const res = await fetch(`${ML_API_BASE}/generate-weekly-plan`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ history, preferences }),
  });

  if (!res.ok) {
    throw new Error("ML Generate Plan failed");
  }

  return res.json();
};

