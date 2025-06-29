// services/RecordService.js
import api from './Api';

export const getAllRecords = async () => {
  const response = await api.get('/medical_records/');
  return response;
};

export const getRecordById = async (id) => {
  const response = await api.get(`/medical_records/${id}`);
  return response;
};

export const createRecord = async (recordData) => {
  const response = await api.post('/medical_records/', recordData);
  return response;
};

export const updateRecord = async (id, updatedData) => {
  const response = await api.patch(`/medical_records/${id}`, updatedData);
  return response;
};

export const deleteRecord = async (id) => {
  const response = await api.delete(`/medical_records/${id}`);
  return response;
};