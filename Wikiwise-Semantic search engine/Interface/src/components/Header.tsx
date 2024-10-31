import React from 'react';
import { Grid, Settings } from 'lucide-react';

export function Header() {
  return (
    <header className="p-4 flex justify-end items-center gap-4">
      <a href="#" className="text-sm hover:underline">Gmail</a>
      <a href="#" className="text-sm hover:underline">Images</a>
      <button className="p-2 hover:bg-gray-100 rounded-full">
        <Grid className="w-5 h-5 text-gray-600" />
      </button>
      <button className="p-2 hover:bg-gray-100 rounded-full">
        <Settings className="w-5 h-5 text-gray-600" />
      </button>
      <button className="bg-blue-500 text-white px-6 py-2 rounded-md hover:bg-blue-600 transition-colors">
        Sign in
      </button>
    </header>
  );
}