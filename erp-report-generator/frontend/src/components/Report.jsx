import React, { forwardRef } from 'react';
import { FiCalendar, FiBarChart2, FiAlertTriangle, FiTrendingUp } from 'react-icons/fi';

const Report = forwardRef(({ reportData }, ref) => {
  if (!reportData) {
    return null;
  }

  const { report_text, metrics } = reportData;
  
  // Format the date for the header
  const formatDate = () => {
    const now = new Date();
    return now.toLocaleDateString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  // Process markdown-style formatting to HTML
  const processText = (text) => {
    // Replace ** bold text ** with <strong> tags
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Replace * italic text * with <em> tags
    text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
    
    return text;
  };

  // Split the report text into sections
  const sections = [];
  let currentSection = { title: 'Executive Summary', content: [] };
  
  report_text.split('\n').forEach((paragraph) => {
    if (!paragraph.trim()) return; // Skip empty lines
    
    // Check if it's a heading
    if (paragraph.startsWith('#') || 
        paragraph.trim().endsWith(':') || 
        (paragraph.length < 60 && !paragraph.includes('.') && !paragraph.includes(',')) || 
        paragraph.toUpperCase() === paragraph) {
      // Save the previous section if it has content
      if (currentSection.content.length > 0) {
        sections.push(currentSection);
      }
      // Start a new section
      currentSection = {
        title: paragraph.replace(/^#+\s*/, '').replace(/:$/, ''),
        content: []
      };
    } else {
      // Add to current section content
      currentSection.content.push(paragraph);
    }
  });
  
  // Add the last section if it has content
  if (currentSection.content.length > 0) {
    sections.push(currentSection);
  }

  // Get an icon for a section based on its title
  const getSectionIcon = (title) => {
    const lowercaseTitle = title.toLowerCase();
    if (lowercaseTitle.includes('summary') || lowercaseTitle.includes('overview')) {
      return <FiBarChart2 className="text-blue-600" />;
    } else if (lowercaseTitle.includes('month') || lowercaseTitle.includes('comparison')) {
      return <FiTrendingUp className="text-green-600" />;
    } else if (lowercaseTitle.includes('inventory') || lowercaseTitle.includes('warning')) {
      return <FiAlertTriangle className="text-amber-600" />;
    } else {
      return <FiBarChart2 className="text-blue-600" />;
    }
  };

  return (
    <div 
      ref={ref} 
      className="report-container print:p-0 print:shadow-none bg-white"
      style={{
        width: '210mm',  
        minHeight: '297mm', 
        margin: '0 auto',
        padding: '20mm',
        boxSizing: 'border-box'
      }}
    >
      {/* Report Header */}
      <div className="border-b border-gray-200 pb-6 mb-6">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">ERP Business Report</h1>
          <div className="flex items-center justify-center text-gray-600">
            <FiCalendar className="mr-2" />
            {formatDate()}
          </div>
          
          {metrics?.date_range && (
            <p className="text-sm text-gray-500 mt-2">
              Data Period: {metrics.date_range.start} to {metrics.date_range.end}
            </p>
          )}
        </div>
      </div>
      
      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <div className="bg-blue-50 p-4 rounded-lg">
          <h3 className="text-sm font-semibold text-blue-800 uppercase mb-1">Total Revenue</h3>
          <p className="text-2xl font-bold text-blue-900">
            LKR {metrics?.total_revenue?.toLocaleString() || '0'}
          </p>
        </div>
        
        {metrics?.mom_changes?.revenue_change_percent !== undefined && (
          <div className={`p-4 rounded-lg ${metrics.mom_changes.revenue_change_percent >= 0 ? 'bg-green-50' : 'bg-red-50'}`}>
            <h3 className="text-sm font-semibold uppercase mb-1 
              ${metrics.mom_changes.revenue_change_percent >= 0 ? 'text-green-800' : 'text-red-800'}">
              Revenue Change
            </h3>
            <p className={`text-2xl font-bold ${metrics.mom_changes.revenue_change_percent >= 0 ? 'text-green-900' : 'text-red-900'}`}>
              {metrics.mom_changes.revenue_change_percent >= 0 ? '+' : ''}
              {metrics.mom_changes.revenue_change_percent.toFixed(1)}%
            </p>
          </div>
        )}
        
        {metrics?.top_products?.[0] && (
          <div className="bg-purple-50 p-4 rounded-lg">
            <h3 className="text-sm font-semibold text-purple-800 uppercase mb-1">Top Product</h3>
            <p className="text-xl font-bold text-purple-900">
              {metrics.top_products[0].product_name}
            </p>
            <p className="text-sm text-purple-700">
              LKR {metrics.top_products[0].revenue.toLocaleString()} in revenue
            </p>
          </div>
        )}
      </div>
      
      {/* Report Sections */}
      <div className="report-content space-y-6">
        {sections.map((section, index) => (
          <div key={index} className="border-l-4 border-blue-500 pl-4 py-1">
            <div className="flex items-center mb-3">
              {getSectionIcon(section.title)}
              <h2 className="text-xl font-bold text-gray-800 ml-2">
                {section.title}
              </h2>
            </div>
            <div className="text-gray-700 space-y-3 ml-6">
              {section.content.map((paragraph, pIndex) => (
                <p 
                  key={pIndex} 
                  className="leading-relaxed"
                  dangerouslySetInnerHTML={{ __html: processText(paragraph) }}
                ></p>
              ))}
            </div>
          </div>
        ))}
      </div>
      
      {/* Data Tables */}
      {metrics?.top_products && metrics.top_products.length > 0 && (
        <div className="mt-8 bg-gray-50 p-6 rounded-lg">
          <h3 className="text-lg font-bold text-gray-800 mb-4 flex items-center">
            <FiBarChart2 className="mr-2 text-blue-600" />
            Top Products Performance
          </h3>
          <div className="overflow-x-auto">
            <table className="min-w-full bg-white rounded-lg overflow-hidden">
              <thead className="bg-gray-100">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Product</th>
                  <th className="px-6 py-3 text-right text-xs font-semibold text-gray-600 uppercase">Units Sold</th>
                  <th className="px-6 py-3 text-right text-xs font-semibold text-gray-600 uppercase">Revenue</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {metrics.top_products.map((product, index) => (
                  <tr key={index} className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                    <td className="px-6 py-4 text-sm font-medium text-gray-900">{product.product_name}</td>
                    <td className="px-6 py-4 text-sm text-gray-800 text-right">{product.units_sold.toLocaleString()}</td>
                    <td className="px-6 py-4 text-sm text-gray-800 text-right">${product.revenue.toLocaleString()}</td>
                  </tr>
                ))}
                <tr className="bg-blue-50">
                  <td className="px-6 py-3 text-sm font-bold text-gray-900">Total</td>
                  <td className="px-6 py-3 text-sm font-bold text-gray-900 text-right">
                    {metrics.top_products.reduce((sum, product) => sum + product.units_sold, 0).toLocaleString()}
                  </td>
                  <td className="px-6 py-3 text-sm font-bold text-gray-900 text-right">
                    ${metrics.top_products.reduce((sum, product) => sum + product.revenue, 0).toLocaleString()}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      )}
      
      {/* Footer */}
      <div className="mt-10 pt-6 border-t border-gray-200 text-center text-gray-600 text-sm">
        <p>Generated with AI-Powered ERP Analytics</p>
        <p className="mt-1">Report generated on {formatDate()}</p>
      </div>
    </div>
  );
});

export default Report;