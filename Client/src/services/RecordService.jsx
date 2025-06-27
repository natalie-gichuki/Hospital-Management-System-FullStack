import api from './api'; // Import your fetch wrapper

// Get all medical records
export const getAllRecords = async () => {
  const response = await api.get('/records');
  return response; 
};

// Get a medical record by ID
export const getRecordById = async (id) => {
  const response = await api.get(`/records/${id}`);
  return response;
};

// Create a new medical record
export const createRecord = async (recordData) => {
  const response = await api.post('/records', recordData);
  return response;
};

// Update an existing medical record
export const updateRecord = async (id, updatedData) => {
  const response = await api.patch(`/records/${id}`, updatedData);
  return response;
};

// Delete a medical record
export const deleteRecord = async (id) => {
  const response = await api.delete(`/records/${id}`);
  return response; 
};

