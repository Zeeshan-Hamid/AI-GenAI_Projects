import React from 'react';
import { LucideIcon } from 'lucide-react';

interface WorkflowStepProps {
  icon: LucideIcon;
  title: string;
  description: string;
  step: number;
}

export const WorkflowStep: React.FC<WorkflowStepProps> = ({
  icon: Icon,
  title,
  description,
  step,
}) => {
  return (
    <div className="relative flex flex-col items-center text-center">
      <div className="w-16 h-16 bg-indigo-100 dark:bg-indigo-900/50 rounded-full flex items-center justify-center mb-4 relative">
        <Icon className="w-8 h-8 text-indigo-600 dark:text-indigo-400" />
        <div className="absolute -top-2 -right-2 w-6 h-6 bg-indigo-600 rounded-full flex items-center justify-center">
          <span className="text-sm font-medium text-white">{step}</span>
        </div>
      </div>
      <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">{title}</h3>
      <p className="text-gray-600 dark:text-gray-300">{description}</p>
    </div>
  );
};