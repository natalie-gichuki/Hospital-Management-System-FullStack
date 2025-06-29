// services/DoctorService.js
import api from './Api';

export const getDoctors = async () => {
  return await api.get('/doctors/');
};

export const addDoctor = async (doctorData) => {
  return await api.post('/doctors/', doctorData);
};

export const deleteDoctor = async (id) => {
  return await api.delete(`/doctors/${id}`);
};