import api from './api';

export const getAllRecords = async () => await api.get('/medical_records/');
export const getRecordById = async (id) => await api.get(`/medical_records/${id}`);
export const createRecord = async (data) => await api.post('/medical_records/', data);
export const updateRecord = async (id, data) => await api.patch(`/medical_records/${id}`, data);
export const deleteRecord = async (id) => await api.delete(`/medical_records/${id}`);
export const getRecordsByPatientId = async (patientId) => await api.get(`/patients/${patientId}/records`);