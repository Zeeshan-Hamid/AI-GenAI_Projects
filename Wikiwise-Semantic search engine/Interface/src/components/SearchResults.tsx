import React, { useEffect, useState } from "react";
import axios from "axios";
import { FilterType } from "../App";

interface SearchResult {
  title: string;
  url: string;
  description: string;
  type: FilterType;
}

interface SearchResultsProps {
  query: string;
  visible: boolean;
  activeFilter: FilterType;
}

export function SearchResults({
  query,
  visible,
  activeFilter,
}: SearchResultsProps) {
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);


  useEffect(() => {
    if (!visible || !query.trim()) return;

    const fetchResults = async () => {
      setLoading(true);
      setError(null);

      let endpoint = "";
      if (activeFilter === "bert") endpoint = "http://localhost:8000/bert/search";
      else if (activeFilter === "snowflake") endpoint = "http://localhost:8000/snowflake/search";
      else if (activeFilter === "bge") endpoint = "http://localhost:8000/bge/search";

      try {
        const response = await axios.post(endpoint, { query });
        setSearchResults(response.data.results || []);
      } catch (err) {
        setError("Failed to fetch search results. Please try again later.");
      } finally {
        setLoading(false);
      }
    };

    fetchResults();
  }, [query, visible, activeFilter]);

  if (!visible) return null;

  if (loading) {
    return (
      <div className="w-full max-w-4xl mx-auto mt-8 px-4">
        <p className="text-sm text-white">Loading results for "{query}"...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="w-full max-w-4xl mx-auto mt-8 px-4">
        <p className="text-sm text-red-500">{error}</p>
      </div>
    );
  }

  const filteredResults =
    activeFilter === "all"
      ? searchResults
      : searchResults.filter((result) => result.type === activeFilter);

  return (
    <div className="w-full max-w-4xl mx-auto mt-8 px-4">
      <p className="text-sm text-white mb-4">
        About {filteredResults.length} results for "{query}"
      </p>

      <div className="space-y-8">
        {filteredResults.map((result, index) => (
          <div
            key={index}
            className="bg-darkblue rounded-lg shadow-sm hover:shadow-md transition-shadow p-6">
            <div className="flex-grow">
              <a
                href={result.url}
                className="text-lg font-semibold text-blue-600 hover:underline mb-2 block">
                {result.title}
              </a>
              <p className="text-lightgrey">{result.description}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
