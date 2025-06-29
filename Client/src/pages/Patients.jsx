import React from "react";
import PatientForm from '../components/PatientForm';

const Patients = () => {
  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Our Loved Patients!</h2>
      <PatientForm/>
    </div>
  );
};

export default Patients;

