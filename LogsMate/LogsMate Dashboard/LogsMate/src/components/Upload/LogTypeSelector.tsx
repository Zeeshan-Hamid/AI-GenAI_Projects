import React, { useState } from "react";
import { ChevronDown } from "lucide-react";

const LOG_TYPES = ["HDFS", "Android", "HealthApp"] as const;
type LogType = (typeof LOG_TYPES)[number];

interface LogTypeSelectorProps {
  onSelect: (type: LogType) => void;
}

export const LogTypeSelector: React.FC<LogTypeSelectorProps> = ({
  onSelect,
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedType, setSelectedType] = useState<LogType>("HDFS");

  const handleSelect = (type: LogType) => {
    setSelectedType(type);
    onSelect(type);
    setIsOpen(false);
  };

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between px-4 py-2.5 bg-white dark:bg-gray-900 border border-gray-300 dark:border-gray-700 rounded-lg hover:border-indigo-500 dark:hover:border-indigo-500 transition-colors">
        <span className="text-gray-700 dark:text-gray-200">{selectedType}</span>
        <ChevronDown className="w-5 h-5 text-gray-500 dark:text-gray-400" />
      </button>

      {isOpen && (
        <div className="absolute top-full left-0 right-0 mt-2 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg overflow-hidden z-10">
          {LOG_TYPES.map((type) => (
            <button
              key={type}
              onClick={() => handleSelect(type)}
              className={`w-full px-4 py-2.5 text-left hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors ${
                selectedType === type
                  ? "bg-indigo-50 dark:bg-indigo-900/50 text-indigo-600 dark:text-indigo-400"
                  : "text-gray-700 dark:text-gray-200"
              }`}>
              {type}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};
