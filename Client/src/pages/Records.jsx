import React from "react";
import RecordTable from '../components/RecordTable'

const Records = () => {
  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Medical Records</h2>
      <RecordTable/>
    </div>
  );
};

export default Records;
