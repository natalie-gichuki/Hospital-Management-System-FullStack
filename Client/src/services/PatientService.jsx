import api from './Api';

export const getAllPatients = async () => await api.get('/patients/');
export const getPatientById = async (id) => await api.get(`/patients/${id}`);
export const createPatient = async (data) => await api.post('/patients/', data);
export const deletePatient = async (id) => await api.delete(`/patients/${id}`);
export const getPatientRecords = async (id) => await api.get(`/patients/${id}/records`);