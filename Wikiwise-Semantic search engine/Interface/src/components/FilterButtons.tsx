import React from 'react';
import { FilterType } from '../App';
import { Search, BookOpen, GraduationCap } from 'lucide-react';

interface FilterButtonsProps {
  activeFilter: FilterType;
  setActiveFilter: (filter: FilterType) => void;
  showResults: boolean;
}

export function FilterButtons({ activeFilter, setActiveFilter, showResults }: FilterButtonsProps) {
  return (
    <div className={`flex gap-3 ${showResults ? 'mt-4' : 'mt-6'} justify-center`}>
      <button
        onClick={() => setActiveFilter('bert')}
        className={`px-4 py-2 rounded-full text-sm font-medium flex items-center gap-2 transition-colors ${
          activeFilter === 'bert'
            ? 'bg-blue-100 text-blue-700'
            : 'bg-gray-50 text-gray-700 hover:bg-gray-100'
        }`}
      >
        
        BERT
      </button>
      <button
        onClick={() => setActiveFilter('bge')}
        className={`px-4 py-2 rounded-full text-sm font-medium flex items-center gap-2 transition-colors ${
          activeFilter === 'bge'
            ? 'bg-blue-100 text-blue-700'
            : 'bg-gray-50 text-gray-700 hover:bg-gray-100'
        }`}
      >
        
        Snow Flake
      </button>
      <button
        onClick={() => setActiveFilter('snowflake')}
        className={`px-4 py-2 rounded-full text-sm font-medium flex items-center gap-2 transition-colors ${
          activeFilter === 'snowflake'
            ? 'bg-blue-100 text-blue-700'
            : 'bg-gray-50 text-gray-700 hover:bg-gray-100'
        }`}
      >
        
        BGE-3
      </button>
    </div>
  );
}