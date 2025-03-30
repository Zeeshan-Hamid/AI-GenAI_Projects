import React, { useState, useCallback, useEffect } from "react";
import { UploadArea } from "../Upload/UploadArea";
import { ProgressBar } from "../Upload/ProgressBar";
import { RecentUploads } from "../Upload/RecentUploads";
import { LogTypeSelector } from "../Upload/LogTypeSelector";
import { useNavigate } from "react-router-dom";
import axios from "axios";

interface RecentUpload {
  filename: string;
  size_bytes: number;
  upload_time: string;
}

interface RecentUploadsResponse {
  files: RecentUpload[];
  total_count: number;
}

interface AnalysisResponse {
  filename: string;
  message: string;
  final_summary: string;
}

export const UploadPage: React.FC = () => {
  const navigate = useNavigate();
  const [uploadProgress, setUploadProgress] = useState<{
    file: string;
    progress: number;
  } | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [recentUploads, setRecentUploads] = useState<RecentUpload[]>([]);
  const [currentUploadedFile, setCurrentUploadedFile] = useState<string | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisComplete, setAnalysisComplete] = useState(false);
  const [selectedLogType, setSelectedLogType] = useState<string>("HDFS");

  const formatFileSize = (bytes: number): string => {
    const units = ['B', 'KB', 'MB', 'GB'];
    let size = bytes;
    let unitIndex = 0;
    
    while (size >= 1024 && unitIndex < units.length - 1) {
      size /= 1024;
      unitIndex++;
    }
    
    return `${size.toFixed(1)} ${units[unitIndex]}`;
  };

  const formatUploadTime = (uploadTime: string): string => {
    const uploadDate = new Date(uploadTime);
    const now = new Date();
    const diffInHours = (now.getTime() - uploadDate.getTime()) / (1000 * 60 * 60);

    if (diffInHours < 24) {
      if (diffInHours < 1) {
        const minutes = Math.floor(diffInHours * 60);
        return `${minutes} minute${minutes !== 1 ? 's' : ''} ago`;
      }
      const hours = Math.floor(diffInHours);
      return `${hours} hour${hours !== 1 ? 's' : ''} ago`;
    } else {
      return uploadDate.toLocaleDateString();
    }
  };

  const handleAnalyze = async () => {
    if (!currentUploadedFile) return;

    setIsAnalyzing(true);
    setAnalysisComplete(false);
    setError(null);

    try {
      // Create FormData object for the request
      const formData = new FormData();
      
      // Map the selected log type to the required format
      let logTypeValue = 'hdfs'; // default
      if (selectedLogType === 'Android') {
        logTypeValue = 'android';
      } else if (selectedLogType === 'HealthApp') {
        logTypeValue = 'health';
      }
      
      // Add log_type to the form data
      formData.append('log_type', logTypeValue);
      
      // Log the request information
      console.log("Analyze API Request:", {
        url: `http://localhost:8080/analyze/${encodeURIComponent(currentUploadedFile)}`,
        logType: logTypeValue,
        formData: Object.fromEntries(formData.entries())
      });

      const response = await axios.post<AnalysisResponse>(
        `http://localhost:8080/analyze/${encodeURIComponent(currentUploadedFile)}`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );
      
      // Log the response data
      console.log("Analyze API Response:", response.data);
      
      setIsAnalyzing(false);
      setAnalysisComplete(true);

      // Wait for 1 second to show the success message before redirecting
      setTimeout(() => {
        navigate('/reports', { 
          state: { 
            analysis: response.data,
            timestamp: new Date().toISOString()
          }
        });
      }, 1000);
    } catch (err) {
      setError("Analysis failed. Please try again.");
      setIsAnalyzing(false);
      setAnalysisComplete(false);
      console.error("Analysis error:", err);
    }
  };

  const fetchRecentUploads = async () => {
    try {
      const response = await axios.get<RecentUploadsResponse>('http://localhost:8080/recent-uploads/');
      setRecentUploads(response.data.files.slice(0, 5));
    } catch (err) {
      console.error('Failed to fetch recent uploads:', err);
    }
  };

  useEffect(() => {
    fetchRecentUploads();
  }, []);

  const handleFileUpload = useCallback(async (files: File[]) => {
    const file = files[0];
    
    // Validate file type
    const allowedTypes = [".log", ".txt"];
    const fileExtension = file.name.toLowerCase().substring(file.name.lastIndexOf("."));
    if (!allowedTypes.includes(fileExtension)) {
      setError("Only .log and .txt files are allowed");
      return;
    }

    setError(null);
    setUploadProgress({ file: file.name, progress: 0 });
    setCurrentUploadedFile(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const config = {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        onUploadProgress(progressEvent: { loaded: number; total?: number }) {
          const progress = Math.round(
            (progressEvent.loaded * 100) / (progressEvent.total || 100)
          );
          setUploadProgress((prev) => 
            prev ? { ...prev, progress } : null
          );
        },
      };

      await axios.post("http://localhost:8080/upload/", formData, config);

      // Reset progress after successful upload and refresh recent uploads
      setTimeout(() => {
        setUploadProgress(null);
        setCurrentUploadedFile(file.name);
        fetchRecentUploads();
      }, 1000);
    } catch (err) {
      setError("Failed to upload file. Please try again.");
      setUploadProgress(null);
      setCurrentUploadedFile(null);
      console.error("Upload error:", err);
    }
  }, []);

  const handleLogTypeSelect = (type: string) => {
    console.log("Selected log type:", type);
    setSelectedLogType(type);
  };

  const formattedRecentUploads = recentUploads.map(upload => ({
    id: upload.upload_time,
    fileName: upload.filename,
    size: formatFileSize(upload.size_bytes),
    timestamp: formatUploadTime(upload.upload_time)
  }));

  return (
    <div className="p-6 max-w-5xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
        Upload Logs
      </h1>
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Select the type of log file you want to analyze
        </label>
        <LogTypeSelector onSelect={handleLogTypeSelect} />
      </div>
      
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4">
          {error}
        </div>
      )}
      
      <UploadArea onFileUpload={handleFileUpload} />

      {uploadProgress && (
        <div className="mt-6">
          <ProgressBar
            fileName={uploadProgress.file}
            progress={uploadProgress.progress}
          />
        </div>
      )}

      {isAnalyzing || analysisComplete ? (
        <div className="mt-6">
          <div className="flex flex-col items-center space-y-4">
            {isAnalyzing ? (
              <>
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Analyzing log file...
                </p>
              </>
            ) : analysisComplete && (
              <div className="flex items-center gap-2 text-green-600 dark:text-green-400">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                </svg>
                <p className="text-sm font-medium">Report Analyzed</p>
              </div>
            )}
          </div>
        </div>
      ) : (
        currentUploadedFile && (
          <div className="mt-6">
            <button
              onClick={handleAnalyze}
              className="w-full px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
              disabled={!currentUploadedFile || isAnalyzing}
            >
              Analyze log file
            </button>
          </div>
        )
      )}

      <RecentUploads uploads={formattedRecentUploads} />
    </div>
  );
};
