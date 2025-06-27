const BASE_URL = 'http://localhost:5555/patients';

export const getPatients = async () => {
  const res = await fetch(BASE_URL);
  if (!res.ok) throw new Error("Failed to fetch patients");
  return res.json();
};

export const addPatient = async (patientData) => {
  const res = await fetch(BASE_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(patientData),
  });
  if (!res.ok) throw new Error("Failed to add patient");
  return res.json();
};

export const deletePatient = async (id) => {
  const res = await fetch(`${BASE_URL}/${id}`, {
    method: 'DELETE',
  });
  if (!res.ok) throw new Error("Failed to delete patient");
  return true;
};
// This service handles patient-related API calls.
// It includes functions to get all patients, add a new patient, and delete a patient by