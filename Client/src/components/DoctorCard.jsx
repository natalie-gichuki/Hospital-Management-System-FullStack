function DoctorCard({ doctors = [], onDelete }) {
  return (
    <div className="overflow-x-auto mt-10">
      <table className="w-full border-collapse border border-gray-400 bg-white shadow-md rounded-xl">
        <thead className="bg-gray-100">
          <tr>
            <th className="border px-4 py-2 text-left">Name</th>
            <th className="border px-4 py-2 text-left">Specialization</th>
            <th className="border px-4 py-2 text-left">Contact</th>
            <th className="border px-4 py-2 text-left">Actions</th>
          </tr>
        </thead>
        <tbody>
          {doctors.map((doctor) => (
            <tr key={doctor.id} className="hover:bg-gray-50">
              <td className="border px-4 py-2">{doctor.name}</td>
              <td className="border px-4 py-2">{doctor.specialization}</td>
              <td className="border px-4 py-2">{doctor.contact}</td>
              <td className="border px-4 py-2">
                <button
                  onClick={() => onDelete(doctor.id)}
                  className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600"
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default DoctorCard;
