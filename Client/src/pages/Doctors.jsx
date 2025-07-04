import { useEffect, useState } from "react";
import { getDoctors, addDoctor, deleteDoctor, patchDoctor } from "../services/DoctorService";
import DoctorCard from "../components/DoctorCard";

function Doctors() {
  const [doctors, setDoctors] = useState([]);
  const [newDoctor, setNewDoctor] = useState({ name: "", specialization: "", contact: "" });
  const [editingId, setEditingId] = useState(null);

  useEffect(() => {
    getDoctors().then(setDoctors).catch(console.error);
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingId) {
        const updated = await patchDoctor(editingId, newDoctor);
        setDoctors(doctors.map(doc => (doc.id === editingId ? updated : doc)));
        setEditingId(null);
      } else {
        const created = await addDoctor(newDoctor);
        setDoctors([...doctors, created]);
      }
      setNewDoctor({ name: "", specialization: "", contact: "" });
    } catch (error) {
      console.error(error.message);
    }
  };

  const handleDelete = async (id) => {
    try {
      await deleteDoctor(id);
      setDoctors(doctors.filter(d => d.id !== id));
    } catch (error) {
      console.error(error.message);
    }
  };

  const handleEdit = (doctor) => {
    setNewDoctor({
      name: doctor.name,
      specialization: doctor.specialization,
      contact: doctor.contact,
    });
    setEditingId(doctor.id);
  };

  return (
    <div className="ml-64 p-6 bg-gray-50 min-h-screen">
      <div className="max-w-3xl mx-auto bg-white p-6 rounded-xl shadow-md">
        <h2 className="text-2xl font-bold mb-6 text-blue-900">
          {editingId ? "Edit Doctor" : "Add a New Doctor"}
        </h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="text"
            placeholder="Doctor's Name"
            value={newDoctor.name}
            onChange={(e) => setNewDoctor({ ...newDoctor, name: e.target.value })}
            className="w-full border border-gray-300 rounded p-3 focus:outline-none focus:ring-2 focus:ring-blue-400"
            required
          />
          <input
            type="text"
            placeholder="Specialization"
            value={newDoctor.specialization}
            onChange={(e) => setNewDoctor({ ...newDoctor, specialization: e.target.value })}
            className="w-full border border-gray-300 rounded p-3 focus:outline-none focus:ring-2 focus:ring-blue-400"
            required
          />
          <input
            type="text"
            name="contact"
            placeholder="Contact Info"
            value={newDoctor.contact}
            onChange={(e) => setNewDoctor({ ...newDoctor, contact: e.target.value })}
            className="w-full border border-gray-300 rounded p-3 focus:outline-none focus:ring-2 focus:ring-blue-400"
            required
          />
          <button
            type="submit"
            className="w-full bg-blue-600 text-white font-semibold py-2 px-4 rounded hover:bg-blue-700 transition"
          >
            {editingId ? "Update Doctor" : "Add Doctor"}
          </button>
        </form>
      </div>

      <div className="max-w-6xl mx-auto mt-10">
        <DoctorCard doctors={doctors} onDelete={handleDelete} onEdit={handleEdit} />
      </div>
    </div>
  );
}

export default Doctors;
