import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import {
  HomeIcon,
  ArrowUpTrayIcon,
  DocumentTextIcon,
  ChartBarIcon,
  ArrowLeftOnRectangleIcon
} from '@heroicons/react/24/outline';
import { Activity } from 'lucide-react';

export const Sidebar: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const getCurrentPage = () => {
    const path = location.pathname;
    if (path === '/') return 'home';
    return path.substring(1) as 'upload' | 'reports' | 'visualizations';
  };

  const currentPage = getCurrentPage();

  return (
    <div className="w-64 bg-white dark:bg-gray-950 shadow-lg h-full border-r border-gray-200 dark:border-gray-800">
      <div className="p-4 flex items-center gap-2 border-b border-gray-200 dark:border-gray-800">
        <Activity className="w-7 h-7 text-indigo-600 dark:text-indigo-400" />
        <div>
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white">LogsMate</h2>
          <p className="text-sm text-gray-600 dark:text-gray-400">{user?.email}</p>
        </div>
      </div>
      <nav className="mt-4">
        <Link
          to="/"
          className={`flex items-center px-4 py-3 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 ${
            currentPage === 'home' ? 'bg-indigo-50 dark:bg-indigo-900/20 text-indigo-600 dark:text-indigo-400' : ''
          }`}
        >
          <HomeIcon className={`w-5 h-5 mr-3 ${currentPage === 'home' ? 'text-indigo-600 dark:text-indigo-400' : ''}`} />
          Home
        </Link>
        <Link
          to="/upload"
          className={`flex items-center px-4 py-3 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 ${
            currentPage === 'upload' ? 'bg-indigo-50 dark:bg-indigo-900/20 text-indigo-600 dark:text-indigo-400' : ''
          }`}
        >
          <ArrowUpTrayIcon className={`w-5 h-5 mr-3 ${currentPage === 'upload' ? 'text-indigo-600 dark:text-indigo-400' : ''}`} />
          Upload
        </Link>
        <Link
          to="/reports"
          className={`flex items-center px-4 py-3 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 ${
            currentPage === 'reports' ? 'bg-indigo-50 dark:bg-indigo-900/20 text-indigo-600 dark:text-indigo-400' : ''
          }`}
        >
          <DocumentTextIcon className={`w-5 h-5 mr-3 ${currentPage === 'reports' ? 'text-indigo-600 dark:text-indigo-400' : ''}`} />
          Reports
        </Link>
        <Link
          to="/visualizations"
          className={`flex items-center px-4 py-3 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 ${
            currentPage === 'visualizations' ? 'bg-indigo-50 dark:bg-indigo-900/20 text-indigo-600 dark:text-indigo-400' : ''
          }`}
        >
          <ChartBarIcon className={`w-5 h-5 mr-3 ${currentPage === 'visualizations' ? 'text-indigo-600 dark:text-indigo-400' : ''}`} />
          Visualizations
        </Link>
      </nav>
      <div className="absolute bottom-0 w-64 p-4 border-t border-gray-200 dark:border-gray-800">
        <button
          onClick={handleLogout}
          className="flex items-center w-full px-4 py-3 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-md transition-colors"
        >
          <ArrowLeftOnRectangleIcon className="w-5 h-5 mr-3" />
          Logout
        </button>
      </div>
    </div>
  );
};