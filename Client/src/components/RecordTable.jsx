
import { useEffect, useState } from 'react';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import {
  getAllRecords,
  createRecord,
  updateRecord,
  deleteRecord,
} from '../services/RecordService';
import { getAllPatients } from '../services/PatientService';
import { getDoctors } from '../services/DoctorService';

const RecordForm = () => {
  const [records, setRecords] = useState([]);
  const [patients, setPatients] = useState([]);
  const [doctors, setDoctors] = useState([]);
  const [editingId, setEditingId] = useState(null);
  const [success, setSuccess] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    fetchAll();
  }, []);

  const fetchAll = async () => {
    try {
      const [recordsData, patientsData, doctorsData] = await Promise.all([
        getAllRecords(),
        getAllPatients(),
        getDoctors(),
      ]);
      setRecords(recordsData);
      setPatients(patientsData);
      setDoctors(doctorsData);
    } catch (err) {
      console.error('Fetch error:', err);
    }
  };

  const formik = useFormik({
    initialValues: {
      diagnosis: '',
      treatment: '',
      patient_id: '',
      doctor_id: '',
      date: '',
    },
    validationSchema: Yup.object({
      diagnosis: Yup.string().required('Diagnosis is required'),
      treatment: Yup.string().required('Treatment is required'),
      patient_id: Yup.string().required('Patient is required'),
      doctor_id: Yup.string().required('Doctor is required'),
      date: Yup.string().required('Date is required'),
    }),
    onSubmit: async (values, { resetForm }) => {
      setSuccess('');
      setError('');
      const payload = {
        ...values,
        patient_id: parseInt(values.patient_id),
        doctor_id: parseInt(values.doctor_id),
      };

      try {
        if (editingId) {
          await updateRecord(editingId, payload);
          setSuccess('Record updated successfully.');
        } else {
          await createRecord(payload);
          setSuccess('Record created successfully.');
        }
        resetForm();
        setEditingId(null);
        fetchAll();
      } catch (err) {
        console.error('Save error:', err);
        setError('Failed to save record');
      }
    },
  });

  const handleEdit = (record) => {
    setEditingId(record.id);
    formik.setValues({
      diagnosis: record.diagnosis,
      treatment: record.treatment,
      patient_id: record.patient_id.toString(),
      doctor_id: record.doctor_id.toString(),
      date: record.date.slice(0, 10),
    });
  };

  const handleDelete = async (id) => {
    if (!confirm('Are you sure you want to delete this record?')) return;
    try {
      await deleteRecord(id);
      fetchAll();
    } catch (err) {
      console.error('Delete error:', err);
    }
  };

  return (
    <div className="p-6 ml-64 bg-gray-50 min-h-screen">
      <div className="max-w-6xl mx-auto bg-white shadow rounded-xl p-6">
        <h2 className="text-2xl font-bold mb-4">{editingId ? 'Edit' : 'Create'} Medical Record</h2>

        {error && <p className="text-red-600 mb-2">{error}</p>}
        {success && <p className="text-green-600 mb-2">{success}</p>}

        <div className="max-w-2xl mx-auto p-6 bg-white shadow rounded-xl mb-8">
          <form onSubmit={formik.handleSubmit} className="space-y-3">
            <input
              type="text"
              name="diagnosis"
              placeholder="Diagnosis"
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              value={formik.values.diagnosis}
              className="w-full border px-3 py-2 rounded"
            />
            {formik.touched.diagnosis && formik.errors.diagnosis && (
              <p className="text-red-500 text-sm">{formik.errors.diagnosis}</p>
            )}

            <input
              type="text"
              name="treatment"
              placeholder="Treatment"
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              value={formik.values.treatment}
              className="w-full border px-3 py-2 rounded"
            />
            {formik.touched.treatment && formik.errors.treatment && (
              <p className="text-red-500 text-sm">{formik.errors.treatment}</p>
            )}

            <select
              name="patient_id"
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              value={formik.values.patient_id}
              className="w-full border px-3 py-2 rounded"
            >
              <option value="">Select Patient</option>
              {patients.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.name}
                </option>
              ))}
            </select>
            {formik.touched.patient_id && formik.errors.patient_id && (
              <p className="text-red-500 text-sm">{formik.errors.patient_id}</p>
            )}

            <select
              name="doctor_id"
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              value={formik.values.doctor_id}
              className="w-full border px-3 py-2 rounded"
            >
              <option value="">Select Doctor</option>
              {doctors.map((d) => (
                <option key={d.id} value={d.id}>
                  {d.name}
                </option>
              ))}
            </select>
            {formik.touched.doctor_id && formik.errors.doctor_id && (
              <p className="text-red-500 text-sm">{formik.errors.doctor_id}</p>
            )}

            <input
              type="date"
              name="date"
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              value={formik.values.date}
              className="w-full border px-3 py-2 rounded"
            />
            {formik.touched.date && formik.errors.date && (
              <p className="text-red-500 text-sm">{formik.errors.date}</p>
            )}

            <button
              type="submit"
              className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
            >
              {editingId ? 'Update Record' : 'Save Record'}
            </button>
          </form>
        </div>

        <h3 className="text-3xl font-semibold mb-4">All Medical Records</h3>
        <table className="w-full table-auto border-collapse border border-gray-300">
          <thead>
            <tr className="bg-gray-100">
              <th className="border px-3 py-2 text-left">Diagnosis</th>
              <th className="border px-3 py-2 text-left">Treatment</th>
              <th className="border px-3 py-2 text-left">Patient</th>
              <th className="border px-3 py-2 text-left">Doctor</th>
              <th className="border px-3 py-2 text-left">Date</th>
              <th className="border px-3 py-2 text-left">Actions</th>
            </tr>
          </thead>
          <tbody>
            {records.map((record) => (
              <tr key={record.id} className="hover:bg-gray-50">
                <td className="border px-3 py-2">{record.diagnosis}</td>
                <td className="border px-3 py-2">{record.treatment}</td>
                <td className="border px-3 py-2">
                  {patients.find((p) => p.id === record.patient_id)?.name || 'N/A'}
                </td>
                <td className="border px-3 py-2">
                  {doctors.find((d) => d.id === record.doctor_id)?.name || 'N/A'}
                </td>
                <td className="border px-3 py-2">{record.date}</td>
                <td className="border px-3 py-2">
                  <div className="flex space-x-2">
                    <button
                      onClick={() => handleEdit(record)}
                      className="bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => handleDelete(record.id)}
                      className="bg-red-600 text-white px-3 py-1 rounded hover:bg-red-700"
                    >
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default RecordForm;
