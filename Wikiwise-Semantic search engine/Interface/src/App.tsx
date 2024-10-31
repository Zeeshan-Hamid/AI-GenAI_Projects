import React, { useState } from 'react';
import { Header } from './components/Header';
import { SearchBar } from './components/SearchBar';
import { SearchResults } from './components/SearchResults';
import { Footer } from './components/Footer';
import { Logo } from './components/Logo';
import { FilterButtons } from './components/FilterButtons';

export type FilterType = 'all' | 'bert' | 'bge' | 'snowflake';

function App() {
  const [searchFocused, setSearchFocused] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [showResults, setShowResults] = useState(false);
  const [activeFilter, setActiveFilter] = useState<FilterType>('all');

  const handleSearch = () => {
    if (searchQuery.trim()) {
      setShowResults(true);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 flex flex-col pt-20 pb-20">
      

      <main className="flex-grow flex flex-col items-center px-6">
        <div className={`transition-all ${showResults ? 'mt-8 mb-6' : 'mt-32 mb-8'}`}>
          <Logo />
        </div>

        <div className="w-full max-w-[584px]">
          <SearchBar
            searchQuery={searchQuery}
            searchFocused={searchFocused}
            setSearchQuery={setSearchQuery}
            setSearchFocused={setSearchFocused}
            onSearch={handleSearch}
          />

          <FilterButtons
            activeFilter={activeFilter}
            setActiveFilter={setActiveFilter}
            showResults={showResults}
          />
        </div>

        

        <SearchResults 
          query={searchQuery} 
          visible={showResults} 
          activeFilter={activeFilter}
        />
      </main>

      
    </div>
  );
}

export default App;