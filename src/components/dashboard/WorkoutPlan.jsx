// src/components/dashboard/WorkoutPlan.jsx
import React, { useState, useEffect } from 'react';
import { FaPlus, FaTrash, FaPencilAlt, FaMagic } from 'react-icons/fa';

const DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

const WorkoutPlan = ({ schedule, onStart, onClearDay, onAddExercise, onDeleteExercise, onEditExercise, onUpdateTarget, onGenerateWeek }) => {
  const [activeDay, setActiveDay] = useState('Mon');

  // Ensure schedule exists to prevent crashes
  const currentDayData = schedule?.[activeDay] || { muscle: '', exercises: [] };

  // Set today as active day on mount
  useEffect(() => {
    const today = new Date().toLocaleDateString('en-US', { weekday: 'short' });
    if (DAYS.includes(today)) {
      setActiveDay(today);
    }
  }, []);

  return (
    <div className="lg:col-span-2 bg-slate-800/50 border border-slate-700 rounded-2xl p-6 flex flex-col h-full min-h-[500px]">

      {/* Header & Tabs */}
      <div className="mb-4">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-4">
          <div className="flex items-center gap-3 w-full sm:w-auto justify-between sm:justify-start">
            <h3 className="text-xl font-bold">Weekly Schedule</h3>
            <button
              onClick={onGenerateWeek}
              className="flex items-center gap-2 text-xs font-bold px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 rounded-lg text-white transition-all shadow-lg hover:shadow-indigo-500/30 whitespace-nowrap"
              title="AI Generate Full Week"
            >
              <FaMagic /> AI Generate
            </button>
          </div>
          <div className="flex flex-wrap gap-2 text-xs bg-slate-900/50 p-1 rounded-lg w-full sm:w-auto justify-center sm:justify-end">
            {DAYS.map(day => (
              <button
                key={day}
                onClick={() => setActiveDay(day)}
                className={`flex-1 sm:flex-none text-center px-3 py-1.5 rounded-md transition-all ${activeDay === day
                  ? 'bg-[#a4f16c] text-black font-bold shadow-lg shadow-lime-500/20'
                  : 'text-slate-400 hover:text-white hover:bg-slate-700'
                  }`}
              >
                {day}
              </button>
            ))}
          </div>
        </div>

        {/* Target Muscle Input */}
        <div className="flex items-center gap-3 bg-slate-700/30 p-3 rounded-xl border border-slate-700/50">
          <span className="text-slate-400 text-sm font-medium">Target:</span>
          <input
            type="text"
            placeholder="e.g. Chest & Triceps"
            value={currentDayData.muscle || ''}
            onChange={(e) => onUpdateTarget(activeDay, e.target.value)}
            className="bg-transparent border-none outline-none text-white font-semibold placeholder:text-slate-600 flex-grow"
          />
          <div className="flex items-center gap-2 border-l border-slate-700 pl-3">
            <button onClick={() => onClearDay(activeDay)} title="Clear Day" className="text-slate-500 hover:text-red-500 transition">
              <FaTrash />
            </button>
            <button onClick={() => onAddExercise(activeDay)} title="Add Exercise" className="text-xl text-[#a4f16c] hover:scale-110 transition">
              <FaPlus />
            </button>
          </div>
        </div>
      </div>

      {/* Exercise List */}
      <div className="space-y-3 overflow-y-auto pr-2 flex-grow [&::-webkit-scrollbar]:w-2 [&::-webkit-scrollbar-track]:bg-slate-700/50 [&::-webkit-scrollbar-thumb]:bg-slate-500 [&::-webkit-scrollbar-thumb]:rounded-full [&::-webkit-scrollbar-thumb]:hover:bg-[#a4f16c]">
        {currentDayData.exercises && currentDayData.exercises.length > 0 ? (
          currentDayData.exercises.map(ex => (
            <div key={ex.id} className="group flex items-center gap-4 bg-slate-700/50 p-3 rounded-lg border border-transparent hover:border-slate-600 transition-all">
              <img
                src={ex.imageUrl}
                alt={ex.name}
                className="w-12 h-12 rounded-md object-cover bg-slate-800"
              />
              <div className="flex-grow">
                <p className="font-bold text-slate-200">{ex.name}</p>
                <p className="text-sm text-slate-400">{ex.sets}x{ex.reps} • {ex.rest}s rest</p>
              </div>
              <div className="ml-auto flex items-center gap-3 opacity-0 group-hover:opacity-100 transition-opacity">
                <button
                  onClick={() => onEditExercise(activeDay, ex)}
                  className="text-slate-400 hover:text-[#a4f16c] p-2 hover:bg-slate-700 rounded-full transition"
                >
                  <FaPencilAlt />
                </button>
                <button
                  onClick={() => onDeleteExercise(activeDay, ex.id)}
                  className="text-slate-400 hover:text-red-500 p-2 hover:bg-slate-700 rounded-full transition"
                >
                  <FaTrash />
                </button>
              </div>
            </div>
          ))
        ) : (
          <div className="flex flex-col items-center justify-center h-full text-slate-500 gap-2">
            <p className="text-sm">Rest Day?</p>
            <button onClick={() => onAddExercise(activeDay)} className="text-[#a4f16c] text-sm hover:underline">
              Add a workout
            </button>
          </div>
        )}
      </div>

      {/* Start Button */}
      <button
        onClick={() => onStart(currentDayData, activeDay)}
        className="w-full mt-4 font-bold text-lg text-slate-900 bg-[#a4f16c] hover:bg-[#8cd953] py-3 rounded-lg transition-all disabled:bg-slate-700 disabled:text-slate-500 disabled:cursor-not-allowed shadow-lg shadow-lime-500/20 disabled:shadow-none"
        disabled={!currentDayData.exercises || currentDayData.exercises.length === 0}
      >
        START {activeDay.toUpperCase()} WORKOUT
      </button>
    </div>
  );
};

export default WorkoutPlan;