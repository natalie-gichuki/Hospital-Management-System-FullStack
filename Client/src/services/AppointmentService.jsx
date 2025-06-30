const BASE_URL = 'http://localhost:5000/appointments/';

export const getAppointments = async () => {
  const res = await fetch(BASE_URL);
  if (!res.ok) throw new Error("Failed to fetch appointments");
  return res.json();
};

export const addAppointment = async (appointmentData) => {
  const res = await fetch(BASE_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(appointmentData),
  });
  if (!res.ok) throw new Error("Failed to add appointment");
  return res.json();
};

export const patchAppointment = async (id, appointmentData) => {
  const res = await fetch(`${BASE_URL}${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(appointmentData),
  });

  if (!res.ok) throw new Error("Failed to update appointment");
  return res.json();
};


export const deleteAppointment = async (id) => {
  const res = await fetch(`${BASE_URL}/${id}`, {
    method: 'DELETE',
  });
  if (!res.ok) throw new Error("Failed to delete appointment");
  return true;
};


