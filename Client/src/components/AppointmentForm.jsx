import { useState, useEffect } from "react";
import { addAppointment } from "../services/AppointmentService";
import { getDoctors } from "../services/DoctorService";
import { getPatients } from "../services/PatientService";

function AppointmentForm({ onAdd }) {
  const [formData, setFormData] = useState({
    date: "",
    reason: "",
    doctor_id: "",
    patient_id: "",
  });
  const [doctors, setDoctors] = useState([]);
  const [patients, setPatients] = useState([]);

  useEffect(() => {
    getDoctors().then(setDoctors);
    getPatients().then(setPatients);
  }, []);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const created = await addAppointment(formData);
      onAdd(created);
      setFormData({ date: "", reason: "", doctor_id: "", patient_id: "" });
    } catch (err) {
      console.error(err.message);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-2 border p-4 rounded mb-4">
      <input
        type="date"
        name="date"
        value={formData.date}
        onChange={handleChange}
        className="border p-2 w-full"
        required
      />
      <input
        type="text"
        name="reason"
        value={formData.reason}
        onChange={handleChange}
        placeholder="Reason for appointment"
        className="border p-2 w-full"
        required
      />
      <select
        name="doctor_id"
        value={formData.doctor_id}
        onChange={handleChange}
        className="border p-2 w-full"
        required
      >
        <option value="">Select Doctor</option>
        {doctors.map((doc) => (
          <option key={doc.id} value={doc.id}>
            {doc.name}
          </option>
        ))}
      </select>
      <select
        name="patient_id"
        value={formData.patient_id}
        onChange={handleChange}
        className="border p-2 w-full"
        required
      >
        <option value="">Select Patient</option>
        {patients.map((pat) => (
          <option key={pat.id} value={pat.id}>
            {pat.name}
          </option>
        ))}
      </select>
      <button type="submit" className="bg-green-600 text-white px-4 py-2 rounded">
        Add Appointment
      </button>
    </form>
  );
}

export default AppointmentForm;
// This component allows users to create a new appointment by selecting a date, reason, doctor, and patient.
// It fetches the list of doctors and patients from the server and submits the appointment data to the server when the form is submitted.
// The `onAdd` prop is a callback function that gets