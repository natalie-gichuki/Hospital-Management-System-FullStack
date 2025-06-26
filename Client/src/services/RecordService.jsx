import api from './api'; // your pre-configured axios instance

// Get all medical records
export const getAllRecords = async () => {
  const response = await api.get('/medical_records');
  return response.data;
};

// Get a medical record by ID
export const getRecordById = async (id) => {
  const response = await api.get(`/medical_records/${id}`);
  return response.data;
};

// Create a new medical record
export const createRecord = async (recordData) => {
  const response = await api.post('/medical_records', recordData);
  return response.data;
};

// Update an existing medical record
export const updateRecord = async (id, updatedData) => {
  const response = await api.patch(`/medical_records/${id}`, updatedData);
  return response.data;
};

// Delete a medical record
export const deleteRecord = async (id) => {
  await api.delete(`/medical_records/${id}`);
};
