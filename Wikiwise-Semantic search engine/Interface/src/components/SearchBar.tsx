import React, { KeyboardEvent } from "react";
import axios from "axios"; 
import { Search, Mic, Camera } from "lucide-react";

interface SearchBarProps {
  searchQuery: string;
  searchFocused: boolean;
  setSearchQuery: (query: string) => void;
  setSearchFocused: (focused: boolean) => void;
  onSearch: () => void;
}

export function SearchBar({
  searchQuery,
  searchFocused,
  setSearchQuery,
  setSearchFocused,
  onSearch,
}: SearchBarProps) {
  const handleKeyPress = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && searchQuery.trim()) {
      handleSearch();
    }
  };

  const handleSearch = async () => {
    try {
      const response = await axios.post("http://localhost:8000/search", {
        query: searchQuery,
      });
      console.log("Search response:", response.data);
      onSearch();
    } catch (error) {
      console.error("Error during search:", error);
    }
  };

  return (
    <div className="w-full max-w-[584px] relative">
      <div
        className={`flex items-center px-4 py-3 rounded-full border ${
          searchFocused
            ? "border-blue-500 shadow-lg"
            : "border-gray-200 hover:shadow-md"
        } transition-all duration-200`}>
        <button
          onClick={handleSearch}
          className="hover:bg-gray-100 p-1 rounded-full">
          <Search className="w-5 h-5 text-gray-500 mr-3" />
        </button>
        <input
          type="text"
          placeholder="Enter your search items"
          className="flex-grow outline-none text-white bg-gray-900 text-lg"
          onFocus={() => setSearchFocused(true)}
          onBlur={() => setSearchFocused(false)}
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          onKeyPress={handleKeyPress}
        />
        {searchQuery && (
          <button
            onClick={() => setSearchQuery("")}
            className="text-white text-lg px-2 rounded-sm border-white hover:text-gray-700 mr-2">
            x
          </button>
        )}
        <div className="flex items-center gap-2 ml-2"></div>
      </div>
    </div>
  );
}
