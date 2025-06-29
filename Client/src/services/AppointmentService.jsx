import api from './api';

export const getAppointments = async () => await api.get('/appointments/');
export const addAppointment = async (data) => await api.post('/appointments/', data);
export const deleteAppointment = async (id) => await api.delete(`/appointments/${id}`);