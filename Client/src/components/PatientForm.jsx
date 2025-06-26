import { useEffect, useState } from 'react';
import {
  createPatient,
  getAllPatients,
  deletePatient,
} from '../services/patientService';

const PatientForm = () => {
  const [patients, setPatients] = useState([]);
  const [formData, setFormData] = useState({
    name: '',
    age: '',
    gender: '',
    type: '',
    admission_date: '',
    ward_number: '',
    last_visit_date: '',
  });

  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    fetchPatients();
  }, []);

  const fetchPatients = async () => {
    try {
      const data = await getAllPatients();
      setPatients(data);
    } catch (err) {
      console.error('Error fetching patients:', err);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    const { name, age, gender, type } = formData;

    if (!name || !age || !gender || !type) {
      setError('Name, age, gender, and type are required');
      return;
    }

    // Validate extra fields
    if (type === 'inpatient' && (!formData.admission_date || !formData.ward_number)) {
      setError('Admission date and ward number are required for inpatients');
      return;
    }

    if (type === 'outpatient' && !formData.last_visit_date) {
      setError('Last visit date is required for outpatients');
      return;
    }

    // Build payload
    const payload = {
      name,
      age: parseInt(age),
      gender,
      type,
    };

    if (type === 'inpatient') {
      payload.admission_date = formData.admission_date;
      payload.ward_number = parseInt(formData.ward_number);
    } else if (type === 'outpatient') {
      payload.last_visit_date = formData.last_visit_date;
    }

    try {
      const newPatient = await createPatient(payload);
      setSuccess(`Patient "${newPatient.name}" added`);
      setFormData({
        name: '',
        age: '',
        gender: '',
        type: '',
        admission_date: '',
        ward_number: '',
        last_visit_date: '',
      });
      fetchPatients();
    } catch (err) {
      console.error('Error creating patient:', err);
      setError('Failed to create patient');
    }
  };

  const handleDelete = async (id) => {
    if (!confirm('Are you sure you want to delete this patient?')) return;
    try {
      await deletePatient(id);
      fetchPatients();
    } catch (err) {
      console.error('Delete error:', err);
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-6 bg-white shadow rounded-xl">
      <h2 className="text-2xl font-bold mb-4">Register Patient</h2>

      {error && <p className="text-red-600">{error}</p>}
      {success && <p className="text-green-600">{success}</p>}

      <form onSubmit={handleSubmit} className="space-y-3 mb-6">
        <input
          type="text"
          name="name"
          placeholder="Name"
          value={formData.name}
          onChange={handleChange}
          className="w-full border px-3 py-2 rounded"
        />
        <input
          type="number"
          name="age"
          placeholder="Age"
          value={formData.age}
          onChange={handleChange}
          className="w-full border px-3 py-2 rounded"
        />
        <select
          name="gender"
          value={formData.gender}
          onChange={handleChange}
          className="w-full border px-3 py-2 rounded"
        >
          <option value="">Select Gender</option>
          <option value="Female">Female</option>
          <option value="Male">Male</option>
          <option value="Other">Other</option>
        </select>

        <select
          name="type"
          value={formData.type}
          onChange={handleChange}
          className="w-full border px-3 py-2 rounded"
        >
          <option value="">Select Type</option>
          <option value="inpatient">Inpatient</option>
          <option value="outpatient">Outpatient</option>
        </select>

        {formData.type === 'inpatient' && (
          <>
            <input
              type="date"
              name="admission_date"
              value={formData.admission_date}
              onChange={handleChange}
              className="w-full border px-3 py-2 rounded"
            />
            <input
              type="number"
              name="ward_number"
              placeholder="Ward Number"
              value={formData.ward_number}
              onChange={handleChange}
              className="w-full border px-3 py-2 rounded"
            />
          </>
        )}

        {formData.type === 'outpatient' && (
          <input
            type="date"
            name="last_visit_date"
            value={formData.last_visit_date}
            onChange={handleChange}
            className="w-full border px-3 py-2 rounded"
          />
        )}

        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
        >
          Save Patient
        </button>
      </form>

      <h3 className="text-xl font-semibold mb-2">All Patients</h3>
      {patients.length === 0 ? (
        <p>No patients found.</p>
      ) : (
        <table className="w-full table-auto border-collapse border border-gray-300">
          <thead>
            <tr className="bg-gray-100">
              <th className="border px-3 py-2">Name</th>
              <th className="border px-3 py-2">Age</th>
              <th className="border px-3 py-2">Gender</th>
              <th className="border px-3 py-2">Type</th>
              <th className="border px-3 py-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            {patients.map((patient) => (
              <tr key={patient.id}>
                <td className="border px-3 py-2">{patient.name}</td>
                <td className="border px-3 py-2">{patient.age}</td>
                <td className="border px-3 py-2">{patient.gender}</td>
                <td className="border px-3 py-2 capitalize">{patient.type}</td>
                <td className="border px-3 py-2">
                  <button
                    onClick={() => handleDelete(patient.id)}
                    className="text-red-500 hover:underline"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default PatientForm;
