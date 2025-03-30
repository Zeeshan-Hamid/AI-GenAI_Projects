import React from 'react';
import { Menu, Bell, Settings } from 'lucide-react';
import { LogsMateLogo } from '../LogsMateLogo';
import { ThemeToggle } from '../ThemeToggle';

interface HeaderProps {
  toggleSidebar: () => void;
}

export const Header: React.FC<HeaderProps> = ({ toggleSidebar }) => {
  return (
    <header className="fixed top-0 left-0 right-0 h-16 bg-white dark:bg-gray-950 border-b border-gray-200 dark:border-gray-500 z-50">
      <div className="flex items-center justify-between h-full px-4">
        <div className="flex items-center gap-4">
          <button
            onClick={toggleSidebar}
            className="p-2 hover:bg-gray-100 dark:hover:bg-indigo-900 rounded-lg transition-colors"
          >
            <Menu className="w-6 h-6 text-gray-700 dark:text-gray-200" />
          </button>
          <LogsMateLogo />
        </div>
        <div className="flex items-center gap-4">
          <ThemeToggle />
          <button className="p-2 hover:bg-gray-100 dark:hover:bg-indigo-900 rounded-lg transition-colors relative">
            <Bell className="w-6 h-6 text-gray-700 dark:text-gray-200" />
            <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
          </button>
          <button className="p-2 hover:bg-gray-100 dark:hover:bg-indigo-900 rounded-lg transition-colors">
            <Settings className="w-6 h-6 text-gray-700 dark:text-gray-200" />
          </button>
          <div className="w-8 h-8 rounded-full bg-indigo-600 flex items-center justify-center">
            <span className="text-sm font-medium text-white">ZH</span>
          </div>
        </div>
      </div>
    </header>
  );
};