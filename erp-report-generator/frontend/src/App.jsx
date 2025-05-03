import React, { useState, useRef } from 'react';
import axios from 'axios';
import { FiDownload, FiRefreshCw } from 'react-icons/fi';
import FileUploader from './components/FileUploader';
import Report from './components/Report';
import PrintButton from './components/PrintButton';
import DateRangePicker from './components/DateRangePicker';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [reportData, setReportData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const reportRef = useRef(null);

  const handleFileUpload = (file) => {
    setSelectedFile(file);
    setReportData(null);
    setError(null);
  };

  const downloadTemplate = async () => {
    try {
      const response = await axios.get('http://localhost:8000/download-template', {
        responseType: 'blob'
      });
      
      // Create a URL for the blob
      const url = window.URL.createObjectURL(new Blob([response.data]));
      
      // Create a temporary link and click it to trigger download
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'erp_data_template.csv');
      document.body.appendChild(link);
      link.click();
      
      // Clean up
      link.parentNode.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError('Failed to download template. Please try again.');
      console.error(err);
    }
  };

  const generateReport = async () => {
    if (!selectedFile) {
      setError('Please select a CSV file first');
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', selectedFile);
    
    // Add date range to form data if selected
    if (startDate) {
      formData.append('start_date', startDate.toISOString().split('T')[0]);
    }
    if (endDate) {
      formData.append('end_date', endDate.toISOString().split('T')[0]);
    }

    try {
      const response = await axios.post('http://localhost:8000/generate-report', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      
      setReportData(response.data);
      setLoading(false);
    } catch (err) {
      setLoading(false);
      const errorMessage = err.response?.data?.detail || 'Failed to generate report. Please try again.';
      setError(errorMessage);
      console.error(err);
    }
  };
  
  const resetForm = () => {
    setSelectedFile(null);
    setReportData(null);
    setError(null);
    setStartDate(null);
    setEndDate(null);
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h1 className="text-2xl font-bold text-center text-gray-800 mb-6">
            ERP Report Generator
          </h1>
          
          <div className="no-print">
            <div className="flex flex-col sm:flex-row gap-4 items-center justify-between mb-6">
              <button
                onClick={downloadTemplate}
                className="btn-secondary flex items-center w-full sm:w-auto"
              >
                <FiDownload className="mr-2" />
                Download CSV Template
              </button>
              
              {reportData && (
                <div className="flex gap-2 w-full sm:w-auto">
                  <PrintButton contentRef={reportRef} />
                  <button
                    onClick={resetForm}
                    className="btn-secondary flex items-center"
                  >
                    <FiRefreshCw className="mr-2" />
                    Reset
                  </button>
                </div>
              )}
            </div>
            
            {!reportData && (
              <>
                <FileUploader onFileUpload={handleFileUpload} />
                
                <DateRangePicker 
                  startDate={startDate}
                  endDate={endDate}
                  setStartDate={setStartDate}
                  setEndDate={setEndDate}
                />
                
                <div className="mt-6">
                  <button
                    onClick={generateReport}
                    disabled={!selectedFile || loading}
                    className={`w-full btn-primary ${
                      (!selectedFile || loading) ? 'opacity-50 cursor-not-allowed' : ''
                    }`}
                  >
                    {loading ? 'Generating Report...' : 'Generate Report'}
                  </button>
                </div>
              </>
            )}
            
            {error && (
              <div className="mt-4 p-3 bg-red-100 text-red-700 rounded-md">
                {error}
              </div>
            )}
          </div>
          
          {reportData && <Report reportData={reportData} ref={reportRef} />}
        </div>
      </div>
    </div>
  );
}

export default App;