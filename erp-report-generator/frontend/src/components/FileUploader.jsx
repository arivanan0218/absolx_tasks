import React, { useState, useRef } from 'react';
import { FiUpload, FiFile } from 'react-icons/fi';

const FileUploader = ({ onFileUpload }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type === 'text/csv') {
      setSelectedFile(file);
      onFileUpload(file);
    } else {
      alert('Please select a valid CSV file');
      setSelectedFile(null);
      e.target.value = null;
    }
  };

  const handleClick = () => {
    fileInputRef.current.click();
  };

  return (
    <div className="mt-4">
      <label className="file-input-label" onClick={handleClick}>
        <div className="flex items-center justify-center">
          {selectedFile ? (
            <div className="flex items-center">
              <FiFile className="text-blue-500 w-8 h-8 mr-2" />
              <span className="text-sm text-gray-500">
                Selected: {selectedFile.name}
              </span>
            </div>
          ) : (
            <div className="space-y-1 text-center">
              <FiUpload className="mx-auto h-12 w-12 text-gray-400" />
              <div className="flex text-sm text-gray-600">
                <span className="relative font-medium text-blue-600 hover:text-blue-500">
                  Upload a CSV file
                </span>
                <p className="pl-1">or drag and drop</p>
              </div>
              <p className="text-xs text-gray-500">CSV files only</p>
            </div>
          )}
        </div>
        <input
          ref={fileInputRef}
          type="file"
          className="hidden"
          accept=".csv"
          onChange={handleFileChange}
        />
      </label>
    </div>
  );
};

export default FileUploader;