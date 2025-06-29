import { useEffect, useState } from "react";
import { getDoctors, addDoctor, deleteDoctor } from "../services/DoctorService";
import DoctorCard from "../components/DoctorCard";

function Doctors() {
  const [doctors, setDoctors] = useState([]);
  const [newDoctor, setNewDoctor] = useState({ name: "", specialization: "", contact: "" });
  const [error, setError] = useState(null);

  const fetchDoctors = async () => {
    try {
      const data = await getDoctors();
      setDoctors(data);
      setError(null);
    } catch (err) {
      setError("Failed to load doctors: " + err.message);
    }
  };

  useEffect(() => {
    fetchDoctors();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const created = await addDoctor(newDoctor);
      setDoctors((prev) => [...prev, created]);
      setNewDoctor({ name: "", specialization: "", contact: "" });
      setError(null);
    } catch (error) {
      setError("Failed to add doctor: " + error.message);
    }
  };

  const handleDelete = async (id) => {
    try {
      await deleteDoctor(id);
      setDoctors((prev) => prev.filter((d) => d.id !== id));
    } catch (error) {
      setError("Failed to delete doctor: " + error.message);
    }
  };

  return (
    <div className="ml-64 p-6 bg-gray-50 min-h-screen">
      <div className="max-w-3xl mx-auto bg-white p-6 rounded-xl shadow-md">
        <h2 className="text-2xl font-bold mb-6 text-blue-900">Add a New Doctor</h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="text"
            placeholder="Doctor's Name"
            value={newDoctor.name}
            onChange={(e) => setNewDoctor({ ...newDoctor, name: e.target.value })}
            className="w-full border border-gray-300 rounded p-3"
            required
          />
          <input
            type="text"
            placeholder="Specialization"
            value={newDoctor.specialization}
            onChange={(e) => setNewDoctor({ ...newDoctor, specialization: e.target.value })}
            className="w-full border border-gray-300 rounded p-3"
            required
          />
          <input
            type="text"
            placeholder="Contact Info"
            value={newDoctor.contact}
            onChange={(e) => setNewDoctor({ ...newDoctor, contact: e.target.value })}
            className="w-full border border-gray-300 rounded p-3"
            required
          />
          <button
            type="submit"
            className="w-full bg-blue-600 text-white font-semibold py-2 px-4 rounded hover:bg-blue-700 transition"
          >
            Add Doctor
          </button>
        </form>

        {error && <p className="mt-4 text-red-600 font-semibold">{error}</p>}
      </div>

      <div className="max-w-6xl mx-auto mt-10 grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {doctors.map((doctor) => (
          <DoctorCard key={doctor.id} doctor={doctor} onDelete={handleDelete} />
        ))}
      </div>
    </div>
  );
}

export default Doctors;
