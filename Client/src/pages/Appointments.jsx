import { useEffect, useState } from "react";
import { getAppointments, deleteAppointment } from "../services/AppointmentService";
import AppointmentForm from "../components/AppointmentForm";

function Appointments() {
  const [appointments, setAppointments] = useState([]);

  useEffect(() => {
    getAppointments().then(setAppointments).catch(console.error);
  }, []);

  const handleAdd = (appt) => {
    setAppointments([...appointments, appt]);
  };

  const handleDelete = async (id) => {
    try {
      await deleteAppointment(id);
      setAppointments(appointments.filter((a) => a.id !== id));
    } catch (err) {
      console.error(err.message);
    }
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Appointments</h2>
      <AppointmentForm onAdd={handleAdd} />
      <ul className="space-y-2">
        {appointments.map((a) => (
          <li key={a.id} className="border p-3 rounded shadow">
            <p><strong>Date:</strong> {a.date}</p>
            <p><strong>Reason:</strong> {a.reason}</p>
            <p><strong>Doctor:</strong> {a.doctor?.name || a.doctor_id}</p>
            <p><strong>Patient:</strong> {a.patient?.name || a.patient_id}</p>
            <button
              onClick={() => handleDelete(a.id)}
              className="mt-2 bg-red-500 text-white px-3 py-1 rounded"
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Appointments;
// This code defines a React component for managing appointments.
// It fetches appointments from the server, allows adding new appointments via a form,
// and provides a way to delete existing appointments.