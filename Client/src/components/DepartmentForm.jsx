import React, { useState, useEffect } from 'react';
import Modal from './Modal';
import { getDoctors } from '../services/DoctorService';

const DepartmentForm = ({ isOpen, onClose, onSubmit, department }) => {
  const [name, setName] = useState('');
  const [specialty, setSpecialty] = useState('');
  const [headDoctorId, setHeadDoctorId] = useState('');
  const [doctors, setDoctors] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    if (isOpen) {
      setName(department ? department.name : '');
      setSpecialty(department ? department.specialty : '');
      setHeadDoctorId(department ? department.head_doctor_id : '');
      setError('');
      fetchDoctors();
    } else {
      setName('');
      setSpecialty('');
      setHeadDoctorId('');
    }
  }, [isOpen, department]);

  const fetchDoctors = async () => {
    try {
      const res = await getDoctors();
      setDoctors(res);
    } catch (err) {
      console.error("Failed to fetch doctors:", err);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!name.trim() || !specialty.trim() || !headDoctorId) {
      setError("All fields are required.");
      return;
    }

    onSubmit({
      name,
      specialty,
      head_doctor_id: parseInt(headDoctorId),
    });
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={department ? 'Edit Department' : 'Add New Department'}>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-sm font-medium mb-1">Name</label>
          <input
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="e.g., Cardiology"
            className="w-full px-3 py-2 border rounded-md"
          />
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium mb-1">Specialty</label>
          <input
            value={specialty}
            onChange={(e) => setSpecialty(e.target.value)}
            placeholder="e.g., Heart Care"
            className="w-full px-3 py-2 border rounded-md"
          />
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium mb-1">Head Doctor</label>
          <select
            value={headDoctorId}
            onChange={(e) => setHeadDoctorId(e.target.value)}
            className="w-full px-3 py-2 border rounded-md"
          >
            <option value="">-- Select Doctor --</option>
            {doctors.map((doc) => (
              <option key={doc.id} value={doc.id}>
                Dr. {doc.name}
              </option>
            ))}
          </select>
        </div>

        {error && <p className="text-red-500 text-sm">{error}</p>}

        <div className="flex justify-end mt-6 space-x-4">
          <button type="button" onClick={onClose} className="px-4 py-2 bg-gray-200 rounded-md">
            Cancel
          </button>
          <button type="submit" className="px-4 py-2 bg-indigo-600 text-white rounded-md">
            Save
          </button>
        </div>
      </form>
    </Modal>
  );
};

export default DepartmentForm;
