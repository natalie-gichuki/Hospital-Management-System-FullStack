import { NavLink, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { FiLogOut } from 'react-icons/fi';

const Navbar = ({ onLogout }) => {
  const [user, setUser] = useState({ username: '', role: '' });
  const navigate = useNavigate();

  useEffect(() => {
    setUser({
      username: localStorage.getItem('username') || '',
      role: localStorage.getItem('role') || '',
    });
  }, []);

  const handleLogout = () => {
    localStorage.clear();
    onLogout && onLogout();
    navigate('/');
  };

  const linkClass = "block py-2 px-4 text-white hover:bg-blue-700 rounded transition-all duration-200";

  return (
    <aside className="fixed top-0 left-0 w-64 h-screen bg-gradient-to-b from-blue-900 to-blue-700 text-white p-4 shadow-2xl flex flex-col justify-between animate-fade-in-left">
      <div>
        <div className="flex flex-col items-center mb-6">
          <img
            src="https://thumbs.dreamstime.com/b/glowing-neon-line-medical-hospital-building-cross-icon-isolated-blue-background-center-health-care-vector-202554064.jpg"
            alt="Hospital Logo"
            className="w-24 h-24 object-contain mb-2 rounded-full border-2 border-white shadow-lg animate-bounce"
          />
          <h1 className="text-3xl font-bold text-center tracking-wide animate-fade-in-down">🏥 HOSPITAL</h1>
        </div>
        <nav className="flex flex-col space-y-2">
          <NavLink to="/" className={linkClass}>Dashboard</NavLink>
          <NavLink to="/doctors" className={linkClass}>Doctors</NavLink>
          <NavLink to="/patients" className={linkClass}>Patients</NavLink>
          <NavLink to="/appointments" className={linkClass}>Appointments</NavLink>
          <NavLink to="/departments" className={linkClass}>Departments</NavLink>
          <NavLink to="/records" className={linkClass}>Medical Records</NavLink>
        </nav>
      </div>
      <div className="p-4 border-t border-blue-800 mt-6">
        <div className="mb-2 text-sm text-blue-200 animate-fade-in-up">
          <span className="font-semibold">User:</span> {user.username || "Unknown"}<br />
          <span className="font-semibold">Role:</span> {user.role || "Unknown"}
        </div>
        <button
          onClick={handleLogout}
          className="w-full py-2 mt-2 bg-red-600 hover:bg-red-700 rounded flex items-center justify-center gap-2 transition-all duration-200 animate-fade-in-up"
        >
          <FiLogOut /> Logout
        </button>
      </div>
    </aside>
  );
};

export default Navbar;
