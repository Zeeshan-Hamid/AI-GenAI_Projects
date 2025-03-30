import React from 'react';
import { BookOpen, PieChart, Zap, Shield } from 'lucide-react';
import { FeatureCard } from './FeatureCard';

export const FeaturesSection: React.FC = () => {
  const features = [
    {
      icon: BookOpen,
      title: 'Knowledge Base Management',
      description: 'Build and maintain a comprehensive knowledge base of log patterns and solutions.',
    },
    {
      icon: PieChart,
      title: 'Detailed Reports',
      description: 'Generate insightful reports with visualizations and actionable recommendations.',
    },
    {
      icon: Zap,
      title: 'Real-time Analysis',
      description: 'Process and analyze logs in real-time with instant pattern recognition.',
    },
    {
      icon: Shield,
      title: 'Security Insights',
      description: 'Identify security threats and vulnerabilities in your application logs.',
    },
  ];

  return (
    <div className="py-10">
      <div className="max-w-5xl mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
            Powerful Features for Log Analysis
          </h2>
          <p className="text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            Everything you need to understand and optimize your application's behavior
            through comprehensive log analysis.
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {features.map((feature) => (
            <FeatureCard key={feature.title} {...feature} />
          ))}
        </div>
      </div>
    </div>
  );
};