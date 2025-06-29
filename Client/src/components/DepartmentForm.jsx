import { useEffect, useState } from 'react';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import {
  getDepartments,
  createDepartment,
  deleteDepartment,
  updateDepartment,
} from '../services/DepartmentService';
import { getDoctors } from '../services/DoctorService';

const DepartmentForm = () => {
  const [departments, setDepartments] = useState([]);
  const [doctors, setDoctors] = useState([]);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    fetchDepartments();
    fetchDoctors();
  }, []);

  const fetchDepartments = async () => {
    try {
      const data = await getDepartments();
      setDepartments(data);
    } catch (err) {
      console.error('Error fetching departments:', err);
      setError('Failed to load departments');
    }
  };

  const fetchDoctors = async () => {
    try {
      const data = await getDoctors();
      setDoctors(data);
    } catch (err) {
      console.error('Error fetching doctors:', err);
      setError('Failed to load doctors');
    }
  };

  const formik = useFormik({
    initialValues: {
      id: '',
      name: '',
      specialty: '',
      headdoctor_id: '',
    },
    validationSchema: Yup.object({
      name: Yup.string().required('Department name is required'),
      specialty: Yup.string().required('Specialty is required'),
      headdoctor_id: Yup.number()
        .typeError('Head doctor must be selected')
        .required('Head doctor is required'),
    }),
    onSubmit: async (values, { resetForm }) => {
      setError('');
      setSuccess('');
      try {
        if (values.id) {
          await updateDepartment(values.id, {
            name: values.name,
            specialty: values.specialty,
            headdoctor_id: parseInt(values.headdoctor_id),
          });
          setSuccess(`Department "${values.name}" updated successfully!`);
        } else {
          const newDept = await createDepartment({
            name: values.name,
            specialty: values.specialty,
            headdoctor_id: parseInt(values.headdoctor_id),
          });
          setSuccess(`Department "${newDept.name}" created successfully!`);
        }

        resetForm();
        fetchDepartments();
      } catch (err) {
        console.error(err);
        setError('Failed to save department');
      }
    },
  });

  const handleDelete = async (id) => {
    if (!confirm('Are you sure you want to delete this department?')) return;
    try {
      await deleteDepartment(id);
      fetchDepartments();
    } catch (err) {
      console.error('Delete error:', err);
      setError('Failed to delete department');
    }
  };

  const handleEdit = (dept) => {
    formik.setValues({
      id: dept.id,
      name: dept.name,
      specialty: dept.specialty,
      headdoctor_id: dept.headdoctor ? String(dept.headdoctor.id) : '',
    });
  };

  return (
    <div className="p-6 ml-64 bg-gray-50 min-h-screen">
      <div className="max-w-6xl mx-auto bg-white shadow rounded-xl p-6">
        <h2 className="text-2xl font-bold mb-4">
          {formik.values.id ? 'Edit Department' : 'Register Department'}
        </h2>

        {error && <p className="text-red-600">{error}</p>}
        {success && <p className="text-green-600">{success}</p>}

        <form onSubmit={formik.handleSubmit} className="space-y-3 max-w-xl">
          <input
            type="text"
            name="name"
            placeholder="Department Name"
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            value={formik.values.name}
            className="w-full border px-3 py-2 rounded"
          />
          {formik.touched.name && formik.errors.name && (
            <p className="text-red-500 text-sm">{formik.errors.name}</p>
          )}

          <input
            type="text"
            name="specialty"
            placeholder="Specialty"
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            value={formik.values.specialty}
            className="w-full border px-3 py-2 rounded"
          />
          {formik.touched.specialty && formik.errors.specialty && (
            <p className="text-red-500 text-sm">{formik.errors.specialty}</p>
          )}

          <select
            name="headdoctor_id"
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            value={formik.values.headdoctor_id}
            className="w-full border px-3 py-2 rounded bg-white"
          >
            <option value="">-- Select Head Doctor --</option>
            {doctors.map((doc) => (
              <option key={doc.id} value={doc.id}>
                {doc.name} ({doc.specialization})
              </option>
            ))}
          </select>

          {formik.touched.headdoctor_id && formik.errors.headdoctor_id && (
            <p className="text-red-500 text-sm">{formik.errors.headdoctor_id}</p>
          )}

          <div className="flex gap-3">
            <button
              type="submit"
              className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
            >
              {formik.values.id ? 'Update Department' : 'Save Department'}
            </button>

            {formik.values.id && (
              <button
                type="button"
                onClick={() => formik.resetForm()}
                className="w-full bg-gray-400 text-white py-2 rounded hover:bg-gray-500"
              >
                Cancel Edit
              </button>
            )}
          </div>
        </form>

        <h3 className="text-3xl font-semibold mt-10 mb-4">All Departments</h3>
        {departments.length === 0 ? (
          <p className="text-gray-600">No departments found.</p>
        ) : (
          <table className="w-full table-auto border-collapse border border-gray-300">
            <thead>
              <tr className="bg-gray-100">
                <th className="border px-3 py-2 text-left">Name</th>
                <th className="border px-3 py-2 text-left">Specialty</th>
                <th className="border px-3 py-2 text-left">Head Doctor</th>
                <th className="border px-3 py-2 text-left">Actions</th>
              </tr>
            </thead>
            <tbody>
              {departments.map((dept) => (
                <tr key={dept.id} className="hover:bg-gray-50">
                  <td className="border px-3 py-2">{dept.name}</td>
                  <td className="border px-3 py-2">{dept.specialty}</td>
                  <td className="border px-3 py-2">
                    {dept.headdoctor?.name || 'Not Assigned'}
                  </td>
                  <td className="border px-3 py-2 space-x-2">
                    <button
                      onClick={() => handleEdit(dept)}
                      className="bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => handleDelete(dept.id)}
                      className="bg-red-600 text-white px-3 py-1 rounded hover:bg-red-700"
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
    </div>
  );
};

export default DepartmentForm;
