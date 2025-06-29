import React, { useState, useEffect } from "react";
import PatientForm from "../components/PatientForm";
import { getAllPatients } from "../services/PatientService";

const Patients = () => {
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    getAllPatients()
      .then(setPatients)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="p-6 ml-64 bg-gray-50 min-h-screen">
      <div className="max-w-4xl mx-auto bg-white p-6 rounded-xl shadow-md">
        <h2 className="text-2xl font-bold mb-4">Our Loved Patients!</h2>
        <PatientForm />
        {loading ? (
          <p className="mt-4 text-gray-500">Loading...</p>
        ) : error ? (
          <p className="text-red-500">Error: {error}</p>
        ) : (
          <ul className="mt-4 space-y-2">
            {patients.map((p) => (
              <li key={p.id} className="border p-3 rounded-md">
                {p.name} — {p.age} — {p.contact}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default Patients;