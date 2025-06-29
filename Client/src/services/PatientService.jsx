// services/PatientService.js
import api from './Api';

export const getAllPatients = async () => {
  const response = await api.get('/patients/');
  return response;
};

export const getPatientById = async (id) => {
  const response = await api.get(`/patients/${id}`);
  return response;
};

export const createPatient = async (patientData) => {
  const response = await api.post('/patients/', patientData);
  return response;
};

export const deletePatient = async (id) => {
  const response = await api.delete(`/patients/${id}`);
  return response;
};

export const getPatientRecords = async (id) => {
  const response = await api.get(`/patients/${id}/records`);
  return response;
};