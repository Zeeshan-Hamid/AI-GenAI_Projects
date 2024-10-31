import React from 'react';
import { BookOpen } from 'lucide-react';

export function Logo() {
  return (
    <div className="flex items-center gap-2">
      <BookOpen className="w-12 h-12 text-blue-600" />
      <div className="text-5xl font-bold tracking-tight">
        <span className="text-blue-600">Wiki</span>
        <span className="text-emerald-600">Wise</span>
      </div>
    </div>
  );
}