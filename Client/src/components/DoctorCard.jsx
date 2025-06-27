function DoctorCard({ doctor, onDelete }) {
  return (
    <div className="border p-4 rounded shadow">
      <h3 className="text-lg font-semibold">{doctor.name}</h3>
      <p>{doctor.specialization}</p>
      <button
        onClick={() => onDelete(doctor.id)}
        className="mt-2 bg-red-500 text-white px-2 py-1 rounded"
      >
        Delete
      </button>
    </div>
  );
}

export default DoctorCard;

