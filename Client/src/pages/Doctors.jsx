import { useEffect, useState } from "react";
import { getDoctors, addDoctor, deleteDoctor } from "../services/DoctorService";
import DoctorCard from "../components/DoctorCard";

function Doctors() {
  const [doctors, setDoctors] = useState([]);
  const [newDoctor, setNewDoctor] = useState({ name: "", specialization: "", contact: "" });


  useEffect(() => {
    getDoctors().then(setDoctors).catch(console.error);
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const created = await addDoctor(newDoctor);
      setDoctors([...doctors, created]);
      setNewDoctor({ name: "", specialization: "" });
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

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Doctors</h2>

      <form onSubmit={handleSubmit} className="space-y-2 mb-6">
        <input
          type="text"
          placeholder="Doctor's Name"
          value={newDoctor.name}
          onChange={(e) => setNewDoctor({ ...newDoctor, name: e.target.value })}
          className="border p-2 w-full"
        />
        <input
          type="text"
          placeholder="Specialization"
          value={newDoctor.specialization}
          onChange={(e) => setNewDoctor({ ...newDoctor, specialization: e.target.value })}
          className="border p-2 w-full"
        />
        <input
          type="text"
          name="contact"
          placeholder="Contact Info"
          value={newDoctor.contact}
          onChange={(e) => setNewDoctor({ ...newDoctor, contact: e.target.value })}
          className="w-full border p-2 rounded"
        />
        <button type="submit" className="bg-blue-500 text-white px-4 py-2">Add Doctor</button>
      </form>

      <div className="grid gap-4">
        {doctors.map((doctor) => (
          <DoctorCard key={doctor.id} doctor={doctor} onDelete={handleDelete} />
        ))}
      </div>
    </div>
  );
}

export default Doctors;
