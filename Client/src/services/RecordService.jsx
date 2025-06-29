// services/RecordService.js
import api from './api';

export const getAllRecords = async () => {
  const response = await api.get('/records/');
  return response;
};

export const getRecordById = async (id) => {
  const response = await api.get(`/records/${id}`);
  return response;
};

export const createRecord = async (recordData) => {
  const response = await api.post('/records/', recordData);
  return response;
};

export const updateRecord = async (id, updatedData) => {
  const response = await api.patch(`/records/${id}`, updatedData);
  return response;
};

export const deleteRecord = async (id) => {
  const response = await api.delete(`/records/${id}`);
  return response;
};