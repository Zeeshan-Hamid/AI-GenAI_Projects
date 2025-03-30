import React, { useCallback } from 'react';
import { Upload } from 'lucide-react';
import { useDropzone } from 'react-dropzone';

interface UploadAreaProps {
  onFileUpload: (files: File[]) => void;
}

export const UploadArea: React.FC<UploadAreaProps> = ({ onFileUpload }) => {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    onFileUpload(acceptedFiles);
  }, [onFileUpload]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  return (
    <div
      {...getRootProps()}
      className={`w-full p-8 border-2 cursor-pointer border-dashed rounded-xl transition-all duration-300 ${
        isDragActive
          ? 'border-indigo-500 bg-indigo-500/10'
          : 'border-gray-300 dark:border-gray-600 hover:border-indigo-500 hover:bg-indigo-500/5'
      }`}
    >
      <input {...getInputProps()} />
      <div className="flex flex-col items-center gap-4">
        <Upload
          className={`w-12 h-12 ${
            isDragActive ? 'text-indigo-500' : 'text-gray-400 dark:text-gray-500'
          }`}
        />
        <div className="text-center">
          <p className="text-lg font-medium text-gray-700 dark:text-gray-200">
            {isDragActive
              ? 'Drop your log files here'
              : 'Drag & drop your log files here'}
          </p>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
            or click to select files from your computer
          </p>
        </div>
      </div>
    </div>
  );
};