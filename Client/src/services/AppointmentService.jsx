import api from './api';

export const getAppointments = async () => {
  return await api.get('/appointments/');
};

export const addAppointment = async (appointmentData) => {
  return await api.post('/appointments/', appointmentData);
};

export const deleteAppointment = async (id) => {
  return await api.delete(`/appointments/${id}`);
};
