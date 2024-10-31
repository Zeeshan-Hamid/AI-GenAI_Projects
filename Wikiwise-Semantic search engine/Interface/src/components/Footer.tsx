import React from 'react';

export function Footer() {
  return (
    <footer className="bg-gray-100 mt-auto">
      <div className="px-6 py-3 border-b border-gray-200">
        <span className="text-gray-600 text-sm">United States</span>
      </div>
      <div className="px-6 py-3 flex flex-col sm:flex-row justify-between">
        <div className="flex gap-6 text-sm text-gray-600">
          <a href="#" className="hover:underline">About</a>
          <a href="#" className="hover:underline">Advertising</a>
          <a href="#" className="hover:underline">Business</a>
          <a href="#" className="hover:underline">How Search works</a>
        </div>
        <div className="flex gap-6 text-sm text-gray-600 mt-3 sm:mt-0">
          <a href="#" className="hover:underline">Privacy</a>
          <a href="#" className="hover:underline">Terms</a>
          <a href="#" className="hover:underline">Settings</a>
        </div>
      </div>
    </footer>
  );
}