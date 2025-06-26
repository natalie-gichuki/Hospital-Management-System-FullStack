// import { NavLink } from 'react-router-dom';

// const Navbar = () => {
//   const linkClass = "block py-2 px-4 text-white hover:bg-blue-700 rounded";

//   return (
//     <aside className="w-64 h-screen bg-blue-900 text-white p-4">
//       <h1 className="text-2xl font-bold mb-6">🏥 HOSPITAL</h1>
//       <nav className="flex flex-col space-y-2">
//         <NavLink to="/" className={linkClass}>Dashboard</NavLink>
//         <NavLink to="/doctors" className={linkClass}>Doctors</NavLink>
//         <NavLink to="/patients" className={linkClass}>Patients</NavLink>
//         <NavLink to="/appointments" className={linkClass}>Appointments</NavLink>
//         <NavLink to="/departments" className={linkClass}>Departments</NavLink>
//         <NavLink to="/records" className={linkClass}>Medical Records</NavLink>
//       </nav>
//     </aside>
//   );
// };

//export default Navbar;

import { NavLink } from 'react-router-dom';

const Navbar = () => {
  const linkClass = "block py-2 px-4 text-white hover:bg-blue-700 rounded";

  return (
    <aside className="fixed top-0 left-0 w-64 h-screen bg-blue-900 text-white p-4">
      <div className="flex flex-col items-center mb-6">
        <img 
          src="https://thumbs.dreamstime.com/b/glowing-neon-line-medical-hospital-building-cross-icon-isolated-blue-background-center-health-care-vector-202554064.jpg" 
          alt="Hospital Logo" 
          className="w-25 h-25 object-contain mb-2 rounded-full border-2 border-black" 
        />
        <h1 className="text-3xl font-bold text-center">🏥 HOSPITAL</h1>
      </div>

      <nav className="flex flex-col space-y-2">
        <NavLink to="/" className={linkClass}>Dashboard</NavLink>
        <NavLink to="/doctors" className={linkClass}>Doctors</NavLink>
        <NavLink to="/patients" className={linkClass}>Patients</NavLink>
        <NavLink to="/appointments" className={linkClass}>Appointments</NavLink>
        <NavLink to="/departments" className={linkClass}>Departments</NavLink>
        <NavLink to="/records" className={linkClass}>Medical Records</NavLink>
      </nav>
    </aside>
  );
};

export default Navbar;
