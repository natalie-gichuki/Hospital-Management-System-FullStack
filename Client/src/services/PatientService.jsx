
// This imports your custom api object that wraps around the fetch API.
// api contains reusable methods: get, post, patch, delete.
import api from './api';

// Get all patients
// Sends a GET request to /patients.
// await pauses until the data is fetched.
// response is already parsed JSON (because api.get does that).
// Returns the list of all patients.
export const getAllPatients = async () => {
  const response = await api.get('/patients');
  return response; 
};

// Get a single patient by ID
export const getPatientById = async (id) => {
  const response = await api.get(`/patients/${id}`);
  return response;
};

// Create a new patient
// Sends a POST request to /patients with patient data (e.g., name, age).
// patientData is passed in as an object and sent as JSON in the body.
// Returns the newly created patient object (as returned by the backend).
export const createPatient = async (patientData) => {
  const response = await api.post('/patients', patientData);
  return response;
};

// Delete a patient by ID
export const deletePatient = async (id) => {
  const response = await api.delete(`/patients/${id}`);
  return response; 
};

// Get a patient's medical records
export const getPatientRecords = async (id) => {
  const response = await api.get(`/patients/${id}/records`);
  return response;
};


