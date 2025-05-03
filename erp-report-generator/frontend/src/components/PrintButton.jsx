import React from 'react';
import { FiPrinter } from 'react-icons/fi';
import { useReactToPrint } from 'react-to-print';

const PrintButton = ({ contentRef }) => {
  const handlePrint = useReactToPrint({
    content: () => contentRef.current,
    documentTitle: 'ERP Business Report',
  });

  return (
    <button 
      onClick={handlePrint}
      className="btn-primary flex items-center"
    >
      <FiPrinter className="mr-2" />
      Print Report
    </button>
  );
};

export default PrintButton;