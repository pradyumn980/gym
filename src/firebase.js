// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

import { getFirestore } from "firebase/firestore";
// Note: You don't need getAnalytics for auth

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyA6XkRXcX5VfDq0AMdDYcKq1mBG12E08OE",
  authDomain: "mygym-e6283.firebaseapp.com",
  projectId: "mygym-e6283",
  storageBucket: "mygym-e6283.firebasestorage.app",
  messagingSenderId: "6596125260",
  appId: "1:6596125260:web:31359145fe948c0ce2cae9"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase Authentication and export it
export const auth = getAuth(app);
export const db = getFirestore(app);