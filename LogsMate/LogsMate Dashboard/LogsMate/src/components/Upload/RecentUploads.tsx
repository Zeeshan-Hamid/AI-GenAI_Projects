import React from 'react';
import { File } from 'lucide-react';

interface Upload {
  id: string;
  fileName: string;
  size: string;
  timestamp: string;
}

interface RecentUploadsProps {
  uploads: Upload[];
}

export const RecentUploads: React.FC<RecentUploadsProps> = ({ uploads }) => {
  return (
    <div className="bg-white dark:bg-[#101930f6] dark:border-white rounded-xl p-6 shadow-sm">
      <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
        Recent Uploads
      </h2>
      <div className="space-y-4">
        {uploads.map((upload) => (
          <div
            key={upload.id}
            className="flex cursor-pointer items-center gap-4 p-4 rounded-lg bg-gray-50 dark:bg-indigo-600 hover:bg-gray-100 dark:hover:bg-indigo-400 transition-colors">
            <File className="w-6 h-6 text-indigo-600 dark:text-white" />
            <div className="flex-1">
              <h3 className="text-gray-800 dark:text-gray-200 font-medium">
                {upload.fileName}
              </h3>
              <p className="text-sm text-gray-500 dark:text-white">
                {upload.size} • {upload.timestamp}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};