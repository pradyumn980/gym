import { collection, getDocs } from "firebase/firestore";
import { auth, db } from "../firebase";

export const getUserHistory = async () => {
  const user = auth.currentUser;
  if (!user) return [];

  const snapshot = await getDocs(
    collection(db, "users", user.uid, "workouts")
  );

  return snapshot.docs.map(doc => ({
    name: doc.data().name
  }));
};
