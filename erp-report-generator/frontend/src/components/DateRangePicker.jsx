import React from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';

const DateRangePicker = ({ startDate, endDate, setStartDate, setEndDate }) => {
  return (
    <div className="flex flex-col sm:flex-row gap-4 mt-4">
      <div className="w-full sm:w-1/2">
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Start Date (Optional)
        </label>
        <DatePicker
          selected={startDate}
          onChange={(date) => setStartDate(date)}
          selectsStart
          startDate={startDate}
          endDate={endDate}
          className="w-full p-2 border border-gray-300 rounded-md"
          placeholderText="Select start date"
          dateFormat="yyyy-MM-dd"
          isClearable
        />
      </div>
      <div className="w-full sm:w-1/2">
        <label className="block text-sm font-medium text-gray-700 mb-1">
          End Date (Optional)
        </label>
        <DatePicker
          selected={endDate}
          onChange={(date) => setEndDate(date)}
          selectsEnd
          startDate={startDate}
          endDate={endDate}
          minDate={startDate}
          className="w-full p-2 border border-gray-300 rounded-md"
          placeholderText="Select end date"
          dateFormat="yyyy-MM-dd"
          isClearable
          disabled={!startDate}
        />
      </div>
    </div>
  );
};

export default DateRangePicker;