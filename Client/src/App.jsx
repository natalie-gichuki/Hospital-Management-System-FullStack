import { useState } from "react";
import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Patients from "./pages/Patients";
import Doctors from "./pages/Doctors";
import Appointments from "./pages/Appointments";
import Departments from "./pages/Departments";
import Records from "./pages/Records";
import AuthCard from "./components/AuthCard";

const App = () => {
  // <--- CHANGED: Check for 'user_id' or 'username' instead of 'token'
  // 'user_id' is a good indicator that a user is considered logged in.
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem("user_id"));

  const handleLogout = () => {
    // <--- NOTE: localStorage.clear() removes ALL items.
    // If you only want to remove authentication-related items,
    // explicitly remove them:
    // localStorage.removeItem("user_id");
    // localStorage.removeItem("role");
    // localStorage.removeItem("username");
    localStorage.clear(); // Keeping this as per your original code for now
    setIsLoggedIn(false);
  };

  const handleLogin = () => setIsLoggedIn(true);

  if (!isLoggedIn) {
    // Pass handleLogin to AuthCard
    return <AuthCard onLogin={handleLogin} />;
  }

  return (
    <div className="flex">
      <Navbar onLogout={handleLogout} />
      <div className="flex-1 min-h-screen bg-gray-50">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/patients/" element={<Patients />} />
          <Route path="/doctors/" element={<Doctors />} />
          <Route path="/appointments/" element={<Appointments />} />
          <Route path="/departments/" element={<Departments />} />
          <Route path="/records/" element={<Records />} />
        </Routes>
      </div>
    </div>
  );
};

export default App;