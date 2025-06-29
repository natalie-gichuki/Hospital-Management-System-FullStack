import api from './api';

export const getDepartments = async () => await api.get('/departments/');
export const createDepartment = async (data) => await api.post('/departments/', data);
export const updateDepartment = async (id, data) => await api.patch(`/departments/${id}`, data);
export const deleteDepartment = async (id) => await api.delete(`/departments/${id}`);