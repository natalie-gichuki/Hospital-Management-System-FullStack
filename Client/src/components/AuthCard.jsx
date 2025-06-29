// src/components/AuthCard.jsx
import { useState } from "react";
import Login from "./Login";
import Register from "./Register";

const AuthCard = ({ onLogin }) => {
  const [showRegister, setShowRegister] = useState(false);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-900 via-blue-700 to-blue-400 animate-gradient-x">
      <div className="w-full max-w-lg bg-white bg-opacity-90 rounded-2xl shadow-2xl p-10 transition-all duration-500 ease-in-out transform animate-fade-in-up">
        <div className="flex justify-center mb-8">
          <button
            className={`px-6 py-2 rounded-l-lg font-semibold transition-all duration-300 ${
              !showRegister
                ? "bg-blue-700 text-white shadow"
                : "bg-blue-100 text-blue-700 hover:bg-blue-200"
            }`}
            onClick={() => setShowRegister(false)}
          >
            Login
          </button>
          <button
            className={`px-6 py-2 rounded-r-lg font-semibold transition-all duration-300 ${
              showRegister
                ? "bg-green-600 text-white shadow"
                : "bg-green-100 text-green-700 hover:bg-green-200"
            }`}
            onClick={() => setShowRegister(true)}
          >
            Register
          </button>
        </div>
        <div className="transition-all duration-500">
          {showRegister ? (
            <Register onRegister={() => setShowRegister(false)} />
          ) : (
            <Login onLogin={onLogin} />
          )}
        </div>
      </div>
    </div>
  );
};

export default AuthCard;