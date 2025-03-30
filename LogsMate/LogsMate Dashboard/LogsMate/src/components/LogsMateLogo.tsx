import React from 'react';
import { Activity } from 'lucide-react';

export const LogsMateLogo: React.FC = () => {
  return (
    <div className="flex items-center gap-2">
      <Activity className="w-8 h-8 text-indigo-600 dark:text-indigo-400" />
      <span className="text-xl font-bold text-gray-900 dark:text-white">LogsMate</span>
    </div>
  );
};