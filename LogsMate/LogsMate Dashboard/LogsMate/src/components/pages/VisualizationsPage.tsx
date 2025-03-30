import React from 'react';

export const VisualizationsPage: React.FC = () => {
  const grafanaUrl = 'http://localhost:3000/d/ceg8ww5ppgs8wa/logsmate-analysis-dashboard?orgId=1&from=2025-03-18T19:00:00.000Z&to=2025-03-20T18:59:59.000Z&timezone=browser&refresh=5s';

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
        Visualizations Dashboard
      </h1>
      
      <p className="text-gray-600 dark:text-gray-300">
        
      </p>
      
      <div className="relative bg-white dark:bg-gray-800 shadow rounded-lg overflow-hidden">
        <div className="aspect-w-16 aspect-h-9 w-full">
          <iframe
            src={grafanaUrl}
            className="w-full h-[calc(100vh-200px)] border-0"
            title="LogsMate Analytics Dashboard"
            allowFullScreen
          />
        </div>
      </div>
    </div>
  );
}; 