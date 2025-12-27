import { addDoc, collection } from "firebase/firestore";
import { auth, db } from "../firebase";
import { getWorkoutRecommendation } from "./mlService";

export const generateAndSaveRecommendation = async (history) => {
  const user = auth.currentUser;
  if (!user) throw new Error("User not logged in");

  if (!history || history.length === 0) {
    throw new Error("No workout history available for ML");
  }

  // Send only required data to ML
  const formattedHistory = history.map(h => ({
    name: h.originalPlanName || h.name
  }));

  // Call ML API
  const recommendation = await getWorkoutRecommendation(
    formattedHistory,
    "beginner"
  );

  // Save recommendation
  await addDoc(
    collection(db, "users", user.uid, "recommendations"),
    {
      ...recommendation,
      createdAt: new Date(),
    }
  );

  return recommendation;
};
