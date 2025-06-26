import api from './api';

// Get all patients
export const getAllPatients = async () => {
  const response = await api.get('/patients');
  return response.data;
};

// Get a single patient by ID
export const getPatientById = async (id) => {
  const response = await api.get(`/patients/${id}`);
  return response.data;
};

// Create a new patient
export const createPatient = async (patientData) => {
  const response = await api.post('/patients', patientData);
  return response.data;
};

// Delete a patient by ID
export const deletePatient = async (id) => {
  const response = await api.delete(`/patients/${id}`);
  return response.data;
};

// Get a patient's medical records
export const getPatientRecords = async (id) => {
  const response = await api.get(`/patients/${id}/records`);
  return response.data;
};


