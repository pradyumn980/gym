import React, { useState } from 'react';
import { FaTimes, FaDumbbell, FaFire, FaStopwatch } from 'react-icons/fa';

const GenerateWeekModal = ({ isOpen, onClose, onGenerate }) => {
    const [days, setDays] = useState(4);
    const [goal, setGoal] = useState('build_muscle');

    if (!isOpen) return null;

    const handleSubmit = () => {
        onGenerate({
            days_per_week: days,
            goal: goal
        });
        onClose();
    };

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-fade-in">
            <div className="bg-slate-800 border border-slate-700 w-full max-w-md rounded-2xl p-6 shadow-2xl relative">
                <button
                    onClick={onClose}
                    className="absolute top-4 right-4 text-slate-400 hover:text-white transition"
                >
                    <FaTimes />
                </button>

                <h2 className="text-2xl font-bold mb-2 flex items-center gap-2">
                    <FaDumbbell className="text-[#a4f16c]" /> AI Plan Generator
                </h2>
                <p className="text-slate-400 text-sm mb-6">
                    Customize your weekly schedule. The AI will build a plan based on these preferences.
                </p>

                {/* Days Per Week */}
                <div className="mb-6">
                    <label className="block text-sm font-bold mb-2 text-slate-200">
                        Training Days per Week
                    </label>
                    <div className="flex justify-between gap-2 bg-slate-900/50 p-2 rounded-xl border border-slate-700">
                        {[3, 4, 5, 6].map((num) => (
                            <button
                                key={num}
                                onClick={() => setDays(num)}
                                className={`flex-1 py-2 rounded-lg font-bold transition-all ${days === num
                                        ? 'bg-[#a4f16c] text-black shadow-lg shadow-lime-500/20'
                                        : 'text-slate-400 hover:text-white hover:bg-slate-700'
                                    }`}
                            >
                                {num} Days
                            </button>
                        ))}
                    </div>
                    <p className="text-xs text-slate-500 mt-2 text-center">
                        {days === 3 && "Full Body (Mon/Wed/Fri)"}
                        {days === 4 && "Upper / Lower Split"}
                        {days === 5 && "Hybrid (PPL + Upper/Lower)"}
                        {days === 6 && "PPL x2 (Push/Pull/Legs)"}
                    </p>
                </div>

                {/* Goal Selection */}
                <div className="mb-8">
                    <label className="block text-sm font-bold mb-2 text-slate-200">
                        Primary Goal
                    </label>
                    <div className="space-y-2">
                        <button
                            onClick={() => setGoal('build_muscle')}
                            className={`w-full flex items-center gap-3 p-3 rounded-xl border transition-all ${goal === 'build_muscle'
                                    ? 'bg-slate-700 border-[#a4f16c] ring-1 ring-[#a4f16c]'
                                    : 'bg-slate-900/40 border-slate-700 hover:border-slate-500'
                                }`}
                        >
                            <div className={`p-2 rounded-full ${goal === 'build_muscle' ? 'bg-[#a4f16c] text-black' : 'bg-slate-800 text-slate-400'}`}>
                                <FaDumbbell />
                            </div>
                            <div className="text-left">
                                <p className="font-bold text-sm">Build Muscle</p>
                                <p className="text-xs text-slate-400">Standard volume, focus on hypertrophy.</p>
                            </div>
                        </button>

                        <button
                            onClick={() => setGoal('lose_weight')}
                            className={`w-full flex items-center gap-3 p-3 rounded-xl border transition-all ${goal === 'lose_weight'
                                    ? 'bg-slate-700 border-[#a4f16c] ring-1 ring-[#a4f16c]'
                                    : 'bg-slate-900/40 border-slate-700 hover:border-slate-500'
                                }`}
                        >
                            <div className={`p-2 rounded-full ${goal === 'lose_weight' ? 'bg-[#a4f16c] text-black' : 'bg-slate-800 text-slate-400'}`}>
                                <FaFire />
                            </div>
                            <div className="text-left">
                                <p className="font-bold text-sm">Lose Weight / Tone</p>
                                <p className="text-xs text-slate-400">Higher reps, less rest, increased intensity.</p>
                            </div>
                        </button>

                        <button
                            onClick={() => setGoal('strength')}
                            className={`w-full flex items-center gap-3 p-3 rounded-xl border transition-all ${goal === 'strength'
                                    ? 'bg-slate-700 border-[#a4f16c] ring-1 ring-[#a4f16c]'
                                    : 'bg-slate-900/40 border-slate-700 hover:border-slate-500'
                                }`}
                        >
                            <div className={`p-2 rounded-full ${goal === 'strength' ? 'bg-[#a4f16c] text-black' : 'bg-slate-800 text-slate-400'}`}>
                                <FaStopwatch />
                            </div>
                            <div className="text-left">
                                <p className="font-bold text-sm">Strength</p>
                                <p className="text-xs text-slate-400">Lower reps, longer rest, heavy focus.</p>
                            </div>
                        </button>
                    </div>
                </div>

                <button
                    onClick={handleSubmit}
                    className="w-full py-4 bg-[#a4f16c] hover:bg-[#8cd953] text-black font-bold text-lg rounded-xl shadow-lg shadow-lime-500/20 transition-all hover:scale-[1.02] active:scale-[0.98]"
                >
                    Generate Plan ⚡
                </button>
            </div>
        </div>
    );
};

export default GenerateWeekModal;
