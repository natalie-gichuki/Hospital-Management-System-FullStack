import { useEffect, useState } from 'react';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import {
    getAllRecords,
    createRecord,
    updateRecord,
    deleteRecord,
} from '../services/RecordService';

// Imports helper functions to fetch lists of patients and doctors.
import { getAllPatients } from '../services/PatientService';
//import { getAllDoctors } from '../services/DoctorService';

const RecordForm = () => {
    // records: list of medical records
    // patients: patient data
    // doctors: doctor data
    // editingId: track which record is being edited
    // success: success message
    // error: error message

    const [records, setRecords] = useState([]);
    const [patients, setPatients] = useState([]);
    const [doctors, setDoctors] = useState([]);
    const [editingId, setEditingId] = useState(null);
    const [success, setSuccess] = useState('');
    const [error, setError] = useState('');

    useEffect(() => {
        fetchAll();
    }, []);


    // Declares a function to fetch all records, patients, and doctors.

    const fetchAll = async () => {
        try {
            const [recordsData, patientsData, doctorsData] = await Promise.all([
                getAllRecords(),
                getAllPatients(),
                //getAllDoctors(),
            ]);
            // Updates the component state with the fetched data.
            setRecords(recordsData);
            setPatients(patientsData);
            //   setDoctors(doctorsData);
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
                // Decides whether to update an existing record or create a new one.

                if (editingId) {
                    await updateRecord(editingId, payload);
                    setSuccess('Record updated successfully.');
                } else {
                    await createRecord(payload);
                    setSuccess('Record created successfully.');
                }

                // Resets the form, exits edit mode, and refreshes the records list.
                resetForm();
                setEditingId(null);
                fetchAll();
            } catch (err) {
                console.error('Save error:', err);
                setError('Failed to save record');
            }
        },
    });


    // Prefills form fields with record data for editing.
    const handleEdit = (record) => {
        setEditingId(record.id);
        // Sets Formik values from the selected record.
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
        <div className="max-w-3xl mx-auto p-6 bg-white rounded shadow">
            <h2 className="text-2xl font-bold mb-4">{editingId ? 'Edit' : 'Create'} Medical Record</h2>

            {success && <p className="text-green-600">{success}</p>}
            {error && <p className="text-red-600">{error}</p>}

            <form onSubmit={formik.handleSubmit} className="space-y-3 mb-6">
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

            <h3 className="text-xl font-semibold mb-2">All Medical Records</h3>
            <table className="w-full table-auto border-collapse border border-gray-300">
                <thead>
                    <tr className="bg-gray-100">
                        <th className="border px-3 py-2">Diagnosis</th>
                        <th className="border px-3 py-2">Treatment</th>
                        <th className="border px-3 py-2">Patient</th>
                        <th className="border px-3 py-2">Doctor</th>
                        <th className="border px-3 py-2">Date</th>
                        <th className="border px-3 py-2">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {records.map((record) => (
                        <tr key={record.id}>
                            <td className="border px-3 py-2">{record.diagnosis}</td>
                            <td className="border px-3 py-2">{record.treatment}</td>
                            <td className="border px-3 py-2">
                                {patients.find(p => p.id === record.patient_id)?.name || 'N/A'}
                            </td>
                            <td className="border px-3 py-2">
                                {doctors.find(d => d.id === record.doctor_id)?.name || 'N/A'}
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
    );
};

export default RecordForm;


