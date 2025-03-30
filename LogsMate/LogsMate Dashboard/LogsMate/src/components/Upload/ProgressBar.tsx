import React from 'react';

interface ProgressBarProps {
  progress: number;
  fileName: string;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({ progress, fileName }) => {
  return (
    <div className="w-full">
      <div className="flex justify-between mb-2">
        <span className="text-sm text-gray-600 dark:text-gray-300">{fileName}</span>
        <span className="text-sm text-gray-600 dark:text-gray-300">{progress}%</span>
      </div>
      <div className="h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
        <div
          className="h-full bg-indigo-500 transition-all duration-300"
          style={{ width: `${progress}%` }}
        />
      </div>
    </div>
  );
};