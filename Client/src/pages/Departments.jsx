import React, { useState, useEffect, useCallback } from 'react';
import { getDepartments, createDepartment, updateDepartment, deleteDepartment } from '../services/DepartmentService';
import DepartmentForm from '../components/DepartmentForm';
import ConfirmationModal from '../components/ConfirmationModal';
import { FiEdit, FiTrash2, FiPlus } from 'react-icons/fi';

const DepartmentsPage = () => {
    const [departments, setDepartments] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    const [isFormOpen, setIsFormOpen] = useState(false);
    const [isConfirmOpen, setIsConfirmOpen] = useState(false);
    const [selectedDepartment, setSelectedDepartment] = useState(null);

    const fetchDepartments = useCallback(async () => {
        try {
            setIsLoading(true);
            const data = await getDepartments();
            setDepartments(data);
            setError(null);
        } catch (err) {
            setError("Failed to fetch departments: " + err.message);
        } finally {
            setIsLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchDepartments();
    }, [fetchDepartments]);

    const handleAdd = () => {
        setSelectedDepartment(null);
        setIsFormOpen(true);
    };

    const handleEdit = (department) => {
        setSelectedDepartment(department);
        setIsFormOpen(true);
    };

    const handleDelete = (department) => {
        setSelectedDepartment(department);
        setIsConfirmOpen(true);
    };

    const handleFormSubmit = async (departmentData) => {
        try {
            if (selectedDepartment) {
                await updateDepartment(selectedDepartment.id, departmentData);
            } else {
                await createDepartment(departmentData);
            }
            fetchDepartments();
            setIsFormOpen(false);
        } catch (err) {
            setError("Failed to save department: " + err.message);
        }
    };

    const handleConfirmDelete = async () => {
        try {
            await deleteDepartment(selectedDepartment.id);
            fetchDepartments();
            setIsConfirmOpen(false);
        } catch (err) {
            setError("Failed to delete department: " + err.message);
        }
    };

    return (
        <div className="p-6 ml-64 bg-gradient-to-br from-blue-50 via-white to-blue-100 min-h-screen animate-fade-in">
            <div className="max-w-6xl mx-auto bg-white shadow-xl rounded-2xl p-8">
                <div className="flex justify-between items-center mb-8">
                    <h1 className="text-3xl font-bold text-blue-800 animate-fade-in-down">Manage Departments</h1>
                    <button
                        onClick={handleAdd}
                        className="flex items-center px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 transition-colors shadow animate-bounce"
                    >
                        <FiPlus className="mr-2" /> Add Department
                    </button>
                </div>

                {isLoading && <p>Loading departments...</p>}
                {error && <p className="text-red-500">Error: {error}</p>}

                {!isLoading && !error && (
                    <div className="bg-white shadow-md rounded-lg overflow-hidden">
                        <table className="min-w-full divide-y divide-gray-200">
                            <thead className="bg-gray-100">
                                <tr>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                                </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-gray-200">
                                {departments.map((dept) => (
                                    <tr key={dept.id} className="hover:bg-gray-50">
                                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{dept.id}</td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{dept.name}</td>
                                        <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                            <button onClick={() => handleEdit(dept)} className="text-indigo-600 hover:text-indigo-900 mr-4"><FiEdit size={18} /></button>
                                            <button onClick={() => handleDelete(dept)} className="text-red-600 hover:text-red-900"><FiTrash2 size={18} /></button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}

                <DepartmentForm
                    isOpen={isFormOpen}
                    onClose={() => setIsFormOpen(false)}
                    onSubmit={handleFormSubmit}
                    department={selectedDepartment}
                />

                <ConfirmationModal
                    isOpen={isConfirmOpen}
                    onClose={() => setIsConfirmOpen(false)}
                    onConfirm={handleConfirmDelete}
                    title="Confirm Deletion"
                    message={`Are you sure you want to delete the "${selectedDepartment?.name}" department? This action cannot be undone.`}
                />
            </div>
        </div>
    );
};

export default DepartmentsPage;
