import api from './api'; // Import your fetch wrapper

// Get all medical records
export const getAllRecords = async () => {
  const response = await api.get('/medical_records');
  return response; 
};

// Get a medical record by ID
export const getRecordById = async (id) => {
  const response = await api.get(`/medical_records/${id}`);
  return response;
};

// Create a new medical record
export const createRecord = async (recordData) => {
  const response = await api.post('/medical_records', recordData);
  return response;
};

// Update an existing medical record
export const updateRecord = async (id, updatedData) => {
  const response = await api.patch(`/medical_records/${id}`, updatedData);
  return response;
};

// Delete a medical record
export const deleteRecord = async (id) => {
  const response = await api.delete(`/medical_records/${id}`);
  return response; 
};

