// services/DepartmentService.js
import api from './api';

export const getDepartments = async () => {
  const res = await api.get('/departments/');
  // The api.get already throws an error if !res.ok, so this check is redundant but harmless.
  // if (!res.ok) throw new Error("Failed to fetch departments"); 
  return res; // api.get already returns res.json()
};

export const createDepartment = async (departmentData) => {
  const res = await api.post('/departments/', departmentData);
  // api.post already handles !res.ok and throws error
  return res; // api.post already returns res.json()
};

export const updateDepartment = async (id, updatedData) => {
  const res = await api.patch(`/departments/${id}`, updatedData);
  // api.patch already handles !res.ok and throws error
  return res; // api.patch already returns res.json()
};

export const deleteDepartment = async (id) => {
  const res = await api.delete(`/departments/${id}`);
  // api.delete already handles !res.ok and throws error
  return res; // api.delete already returns true
};