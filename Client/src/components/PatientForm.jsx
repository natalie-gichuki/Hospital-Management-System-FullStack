// [useEffect] lets the component run side-effects (like fetching data).
// [useState] creates state variables to store patients, error messages, and success messages.
import { useEffect, useState } from 'react';
// [useFormik] initializes and handles the form logic: form state, validation, and submission.
import { useFormik } from 'formik';
// [Yup] is used to define a schema that will validate the form fields.
import * as Yup from 'yup';
// These functions interact with the backend API using fetch (defined in patientService.js).
import { createPatient, getAllPatients, deletePatient } from '../services/PatientService';


// This defines a React functional component named PatientForm.
const PatientForm = () => {
  // [patients] stores the array of all patients fetched from the backend.
  // [setPatients] is the function used to update this array.
  const [patients, setPatients] = useState([]);
  // error and success hold strings used to show feedback messages to the user.
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  
  // This runs fetchPatients() once when the component loads 
  useEffect(() => {
    fetchPatients();
  }, []);
  

  // This function calls the API to get all patients.
  // If successful, it updates the patients state with the response.
  // If it fails, it logs the error and sets an error message.
  const fetchPatients = async () => {
    try {
      const data = await getAllPatients(); // uses fetch
      setPatients(data);
    } catch (err) {
      console.error('Error fetching patients:', err);
      setError('Failed to load patients');
    }
  };
  

  // Sets initial empty values for all form fields.(uses formik)
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

    // Defines validation rules using Yup: all fields are required except those conditionally applied below
    validationSchema: Yup.object({
      name: Yup.string().required('Name is required'),
      age: Yup.number().required('Age is required'),
      gender: Yup.string().required('Gender is required'),
      type: Yup.string().required('Type is required'),

      // Conditional validation: only apply these rules when patient type is "inpatient" or "outpatient".
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

    // This function runs when the user submits the form. It first clears any existing messages.
    onSubmit: async (values, { resetForm }) => {
      setError('');
      setSuccess('');
      
      // Calls the API to create a new patient.
      // Converts age and ward_number from string to number (formik stores form inputs as strings).
      try {
        const newPatient = await createPatient({
          ...values,
          age: parseInt(values.age),
          ward_number: values.ward_number ? parseInt(values.ward_number) : undefined,
        });
        
        // If the API call is successful, shows a success message, resets the form, and reloads the patient list.
        // If it fails, logs the error and sets an error message.
        setSuccess(`Patient "${newPatient.name}" added successfully!`);
        resetForm();
        fetchPatients();
      } catch (err) {
        console.error('Error creating patient:', err);
        setError('Failed to create patient');
      }
    },
  });
  

  // Prompts the user to confirm before deletion.
  const handleDelete = async (id) => {
    if (!confirm('Are you sure you want to delete this patient?')) return;

    // Deletes the patient by ID and reloads the list on success.
    // Logs and sets an error message if deletion fails.
    try {
      await deletePatient(id);
      fetchPatients();
    } catch (err) {
      console.error('Delete error:', err);
      setError('Failed to delete patient');
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-6 bg-white shadow rounded-xl">
      <h2 className="text-2xl font-bold mb-4">Register Patient</h2>

      {error && <p className="text-red-600">{error}</p>}
      {success && <p className="text-green-600">{success}</p>}
      

      {/* The form uses
      <input> for name, age, admission_date, ward_number, and last_visit_date
      <select> for gender and type */}

      {/* Each field includes:
      name: used by Formik to manage value and validation
      value: current value from form state
      onChange, onBlur: connected to Formik
      Error message shown if validation fails */}

      {/* onChange={formik.handleChange}
       This tells the input field how to update the form state whenever the user types into it.
       formik.handleChange is a function that Formik provides. It:
       Listens for user input (onChange event),
       Automatically updates the corresponding value inside formik.values based on the field’s name attribute.
       Example:
       If you type "Alice" into an input with name="name", Formik stores:
       formik.values.name = "Alice". */}

      {/* 👁 onBlur={formik.handleBlur}
       This tracks when the input field loses focus (the user clicks away or tabs out).
       formik.handleBlur:
       Marks the field as "touched".
       This is important for validation — Formik won't show errors for untouched fields.*/}
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
        {/* formik.touched.name
          What it is: A boolean indicating whether the user has focused and then blurred (unfocused) the "name" input field.
          Why it matters: It ensures that error messages only appear after the user interacts with the field (so they don’t see errors immediately on page load).

          ❗ formik.errors.name
          What it is: A string containing the validation error message for the "name" field (if any).
          Where it comes from: Your Yup schema:
          name: Yup.string().required('Name is required')
          If the field is invalid (e.g., left blank), this becomes:
          "Name is required".

          formik.touched.name && formik.errors.name
          This combined condition ensures:
          ✅ The user has touched the field.
          ❌ The field has a validation error.
          If both are true → then the error message will be shown.
          <p className="text-red-500 text-sm">{formik.errors.name}</p>*/}

        <input
          type="text"
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
        

        {/*These inputs only appear if type is 'inpatient'.*/}
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

      <h3 className="text-3xl font-bold mb-2">All Patients</h3>
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


