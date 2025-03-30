import React from 'react';
import { Upload, Search, LineChart } from 'lucide-react';
import { WorkflowStep } from './WorkflowStep';

export const HowItWorksSection: React.FC = () => {
  const steps = [
    {
      icon: Upload,
      title: 'Submit Logs',
      description: 'Upload your log files through our intuitive interface.',
    },
    {
      icon: Search,
      title: 'Analyze Logs',
      description: 'Our AI-powered system processes and analyzes your logs.',
    },
    {
      icon: LineChart,
      title: 'Generate Insights',
      description: 'Get detailed insights and actionable recommendations.',
    },
  ];

  return (
    <div className="py-24 bg-gray-50 dark:bg-gray-950">
      <div className="max-w-5xl mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
            How It Works
          </h2>
          <p className="text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            Three simple steps to transform your log data into valuable insights
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
          {steps.map((step, index) => (
            <WorkflowStep key={step.title} {...step} step={index + 1} />
          ))}
        </div>
      </div>
    </div>
  );
};