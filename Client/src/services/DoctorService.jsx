const BASE_URL = 'http://localhost:5555/doctors';

export const getDoctors = async () => {
  const res = await fetch(BASE_URL);
  if (!res.ok) throw new Error("Failed to fetch doctors");
  return res.json();
};

export const addDoctor = async (doctorData) => {
  const res = await fetch(BASE_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(doctorData),
  });
  if (!res.ok) throw new Error("Failed to add doctor");
  return res.json();
};

export const deleteDoctor = async (id) => {
  const res = await fetch(`${BASE_URL}/${id}`, {
    method: 'DELETE',
  });
  if (!res.ok) throw new Error("Failed to delete doctor");
  return true;
};

