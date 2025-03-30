import React from 'react';
import { Activity, ArrowRight } from 'lucide-react';

export const HeroSection: React.FC = () => {
  return (
    <div className="relative overflow-hidden bg-gradient-to-b from-indigo-900/20 to-transparent py-24">
      <div className="max-w-5xl mx-auto px-6">
        <div className="text-center space-y-8">
          <div className="flex items-center justify-center gap-3 text-indigo-500 dark:text-indigo-400">
            <Activity className="w-8 h-8" />
            <span className="text-xl font-semibold">LogsMate</span>
          </div>
          <h1 className="text-5xl font-bold text-gray-900 dark:text-white">
            Effortless Log Analysis
            <br />
            <span className="text-indigo-600 dark:text-indigo-400">
              for Developers
            </span>
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            Transform complex log data into actionable insights with our
            powerful analysis tools and intelligent pattern recognition.
          </p>
          <div className="flex items-center justify-center gap-4">
            <button className="px-6 py-3 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg font-medium transition-colors flex items-center gap-2">
              Get Started
              <ArrowRight className="w-4 h-4" />
            </button>
            <button className="px-6 py-3 border border-gray-300 dark:border-indigo-600 dark:text-white hover:border-indigo-500 dark:hover:border-indigo-500 rounded-lg font-medium transition-colors">
              Watch Demo
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};