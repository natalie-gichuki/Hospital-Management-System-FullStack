import { useEffect, useState } from "react";
import { getAppointments, deleteAppointment } from "../services/AppointmentService";
import AppointmentForm from "../components/AppointmentForm";

function Appointments() {
  const [appointments, setAppointments] = useState([]);
  const [selectedAppointment, setSelectedAppointment] = useState(null);

  useEffect(() => {
    getAppointments().then(setAppointments).catch(console.error);
  }, []);

  const handleAdd = (appt) => {
    const exists = appointments.find(a => a.id === appt.id);
    if (exists) {
      setAppointments(appointments.map(a => (a.id === appt.id ? appt : a)));
    } else {
      setAppointments([...appointments, appt]);
    }
  };

  const handleDelete = async (id) => {
    try {
      await deleteAppointment(id);
      setAppointments(appointments.filter((a) => a.id !== id));
    } catch (err) {
      console.error(err.message);
    }
  };

  const handleEdit = (appointment) => {
    setSelectedAppointment(appointment);
  };

  return (
    <div className="p-6 ml-64 bg-gray-50 min-h-screen">
      <div className="max-w-6xl mx-auto bg-white shadow rounded-xl p-6">
        <h2 className="text-2xl font-bold mb-4">Appointments</h2>

        <AppointmentForm
          onAdd={handleAdd}
          selectedAppointment={selectedAppointment}
          setSelectedAppointment={setSelectedAppointment}
        />

        <h3 className="text-3xl font-semibold mt-6 mb-2">All Appointments</h3>

        {appointments.length === 0 ? (
          <p className="mt-4 text-gray-600">No appointments found.</p>
        ) : (
          <table className="w-full table-auto border-collapse border border-gray-300">
            <thead>
              <tr className="bg-gray-100">
                <th className="border px-3 py-2">Date</th>
                <th className="border px-3 py-2">Reason</th>
                <th className="border px-3 py-2">Doctor</th>
                <th className="border px-3 py-2">Patient</th>
                <th className="border px-3 py-2">Actions</th>
              </tr>
            </thead>
            <tbody>
              {appointments.map((a) => (
                <tr key={a.id}>
                  <td className="border px-3 py-2">{a.date}</td>
                  <td className="border px-3 py-2">{a.reason}</td>
                  <td className="border px-3 py-2">{a.doctor?.name || a.doctor_id}</td>
                  <td className="border px-3 py-2">{a.patient?.name || a.patient_id}</td>
                  <td className="border px-3 py-2">
                    <div className="flex space-x-2">
                      <button
                        onClick={() => handleEdit(a)}
                        className="bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleDelete(a.id)}
                        className="bg-red-600 text-white px-3 py-1 rounded hover:bg-red-700"
                      >
                        Delete
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default Appointments;
