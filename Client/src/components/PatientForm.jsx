import { useEffect, useState } from 'react';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import { createPatient, getAllPatients, deletePatient} from '../services/patientService';


const PatientForm = () => {
  const [patients, setPatients] = useState([]);
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



  const formik = useFormik({
    initialValues: {
      name: '',
      age: '',
      gender: '',
      type: '',
      admission_date: '',
      ward_number: '',
      last_visit_date: '',
    },
    validationSchema: Yup.object({
      name: Yup.string().required('Name is required'),
      age: Yup.number().required('Age is required'),
      gender: Yup.string().required('Gender is required'),
      type: Yup.string().required('Type is required'),
      admission_date: Yup.string().when('type', {
        is: 'inpatient',
        then: Yup.string().required('Admission date is required'),
      }),
      ward_number: Yup.number().when('type', {
        is: 'inpatient',
        then: Yup.number().required('Ward number is required'),
      }),
      last_visit_date: Yup.string().when('type', {
        is: 'outpatient',
        then: Yup.string().required('Last visit date is required'),
      }),
    }),

    onSubmit: async (values, { resetForm }) => {
      setError('');
      setSuccess('');

      try {
        const newPatient = await createPatient({
          ...values,
          age: parseInt(values.age),
          ward_number: values.ward_number ? parseInt(values.ward_number) : undefined,
        });
        setSuccess(`Patient "${newPatient.name}" added successfully!`);
        resetForm();
        fetchPatients();
      } catch (err) {
        console.error('Error creating patient:', err);
        setError('Failed to create patient');
      }
    },
  });


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

      <form onSubmit={formik.handleSubmit} className="space-y-3 mb-6">
        <input
          type="text"
          name="name"
          placeholder="Name"
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}
          value={formik.values.name}
          className="w-full border px-3 py-2 rounded"
        />
        {formik.touched.name && formik.errors.name && <p className="text-red-500 text-sm">{formik.errors.name}</p>}

        <input
          type="number"
          name="age"
          placeholder="Age"
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}
          value={formik.values.age}
          className="w-full border px-3 py-2 rounded"
        />
        {formik.touched.age && formik.errors.age && <p className="text-red-500 text-sm">{formik.errors.age}</p>}

        <select
          name="gender"
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}
          value={formik.values.gender}
          className="w-full border px-3 py-2 rounded"
        >
          <option value="">Select Gender</option>
          <option value="Female">Female</option>
          <option value="Male">Male</option>
          <option value="Other">Other</option>
        </select>
        {formik.touched.gender && formik.errors.gender && <p className="text-red-500 text-sm">{formik.errors.gender}</p>}

        <select
          name="type"
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}
          value={formik.values.type}
          className="w-full border px-3 py-2 rounded"
        >
          <option value="">Select Type</option>
          <option value="inpatient">Inpatient</option>
          <option value="outpatient">Outpatient</option>
        </select>
        {formik.touched.type && formik.errors.type && <p className="text-red-500 text-sm">{formik.errors.type}</p>}

        {formik.values.type === 'inpatient' && (
          <>
            <input
              type="date"
              name="admission_date"
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              value={formik.values.admission_date}
              className="w-full border px-3 py-2 rounded"
            />
            {formik.touched.admission_date && formik.errors.admission_date && <p className="text-red-500 text-sm">{formik.errors.admission_date}</p>}

            <input
              type="number"
              name="ward_number"
              placeholder="Ward Number"
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              value={formik.values.ward_number}
              className="w-full border px-3 py-2 rounded"
            />
            {formik.touched.ward_number && formik.errors.ward_number && <p className="text-red-500 text-sm">{formik.errors.ward_number}</p>}
          </>
        )}

        {formik.values.type === 'outpatient' && (
          <>
            <input
              type="date"
              name="last_visit_date"
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              value={formik.values.last_visit_date}
              className="w-full border px-3 py-2 rounded"
            />
            {formik.touched.last_visit_date && formik.errors.last_visit_date && <p className="text-red-500 text-sm">{formik.errors.last_visit_date}</p>}
          </>
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

