import { useState, useEffect } from "react";
import { addAppointment, patchAppointment } from "../services/AppointmentService";
import { getDoctors } from "../services/DoctorService";
import { getAllPatients } from "../services/PatientService";

function AppointmentForm({ onAdd, selectedAppointment, setSelectedAppointment }) {
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
    getAllPatients().then(setPatients);
  }, []);

  useEffect(() => {
    if (selectedAppointment) {
      setFormData({
        date: selectedAppointment.date,
        reason: selectedAppointment.reason,
        doctor_id: selectedAppointment.doctor_id.toString(),
        patient_id: selectedAppointment.patient_id.toString(),
      });
    }
  }, [selectedAppointment]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      let appointment;
      if (selectedAppointment) {
        appointment = await patchAppointment(selectedAppointment.id, formData);
        setSelectedAppointment(null); // clear form after editing
      } else {
        appointment = await addAppointment(formData);
      }

      onAdd(appointment);
      setFormData({ date: "", reason: "", doctor_id: "", patient_id: "" });
    } catch (err) {
      console.error(err.message);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white shadow rounded-xl mb-8">
      <h2 className="text-2xl font-bold mb-4">
        {selectedAppointment ? "Edit Appointment" : "Add Appointment"}
      </h2>
      <form onSubmit={handleSubmit} className="space-y-3">
        <input
          type="date"
          name="date"
          value={formData.date}
          onChange={handleChange}
          className="w-full border px-3 py-2 rounded"
          required
        />
        <input
          type="text"
          name="reason"
          value={formData.reason}
          onChange={handleChange}
          placeholder="Reason for appointment"
          className="w-full border px-3 py-2 rounded"
          required
        />
        <select
          name="doctor_id"
          value={formData.doctor_id}
          onChange={handleChange}
          className="w-full border px-3 py-2 rounded"
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
          className="w-full border px-3 py-2 rounded"
          required
        >
          <option value="">Select Patient</option>
          {patients.map((pat) => (
            <option key={pat.id} value={pat.id}>
              {pat.name}
            </option>
          ))}
        </select>
        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
        >
          {selectedAppointment ? "Update Appointment" : "Add Appointment"}
        </button>
      </form>
    </div>
  );
}

export default AppointmentForm;
