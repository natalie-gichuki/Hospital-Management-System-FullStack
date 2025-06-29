// src/components/Login.jsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";
// Removed: import { login } from "../services/AuthService"; // <--- REMOVED THIS IMPORT
import api from "../services/Api"; // <--- NEW: Import the api service

const Login = ({ onLogin }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    try {
      // <--- CHANGED: Direct API call instead of AuthService.login
      // Assuming your login endpoint is still /auth/login as per previous AuthService
      const data = await api.post("/auth/login", { username, password });

      // No access_token to store anymore
      // Removed: localStorage.setItem("access_token", data.access_token);

      // Assuming your backend still returns user_role and user_id with the login response
      // These are stored if your application relies on them for client-side logic/display.
      localStorage.setItem("role", data.user_role);
      localStorage.setItem("user_id", data.user_id);
      localStorage.setItem("username", username); // Store username for display if needed

      setSuccess("Login successful! Redirecting...");
      setTimeout(() => {
        onLogin && onLogin();
        navigate("/");
      }, 1200); // 1.2 seconds delay
    } catch (err) {
      // Error handling remains similar
      console.error("Login failed:", err);
      setError(err.message || "An unexpected error occurred during login.");
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-white bg-opacity-90 p-8 rounded-2xl shadow-2xl w-full animate-fade-in-up"
      style={{ boxShadow: "0 8px 32px 0 rgba(31, 38, 135, 0.37)" }}
    >
      <h2 className="text-3xl font-bold mb-6 text-center text-blue-800 animate-fade-in-down">
        Welcome Back
      </h2>
      {error && (
        <div className="text-red-600 mb-4 text-center">{error}</div>
      )}
      {success && (
        <div className="text-green-600 mb-4 text-center">{success}</div>
      )}
      <div className="mb-4">
        <label htmlFor="login-username" className="block mb-1 font-medium text-blue-800">
          Username
        </label>
        <input
          id="login-username"
          name="username"
          className="block w-full p-3 border border-blue-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
          autoComplete="username"
        />
      </div>
      <div className="mb-6">
        <label htmlFor="login-password" className="block mb-1 font-medium text-blue-800">
          Password
        </label>
        <input
          id="login-password"
          name="password"
          className="block w-full p-3 border border-blue-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          autoComplete="current-password"
        />
      </div>
      <button
        className="w-full py-3 bg-blue-700 hover:bg-blue-900 text-white font-semibold rounded-lg transition-all"
        type="submit"
        disabled={!!success}
      >
        Login
      </button>
    </form>
  );
};

export default Login;