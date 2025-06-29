import api from './Api';

export const getDoctors = async () => await api.get('/doctors/');
export const addDoctor = async (data) => await api.post('/doctors/', data);
export const deleteDoctor = async (id) => await api.delete(`/doctors/${id}`);