// src/components/Register.jsx
import { useState } from 'react';

const Register = ({ onRegister }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('patient');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    try {
      const res = await fetch('http://127.0.0.1:5000/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password, role }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Registration failed');
      setSuccess('Registration successful! You can now log in.');
      onRegister && onRegister(); // Call onRegister to switch back to login form
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white bg-opacity-90 p-8 rounded-2xl shadow-2xl w-full animate-fade-in-up">
      <h2 className="text-3xl font-bold mb-6 text-center text-green-800 animate-fade-in-down">Register</h2>
      {error && <div className="text-red-600 mb-2">{error}</div>}
      {success && <div className="text-green-600 mb-2">{success}</div>}
      <div className="mb-4">
        <label htmlFor="register-username" className="block mb-1 font-medium text-green-800">
          Username
        </label>
        <input
          id="register-username"
          name="username"
          className="block w-full p-3 border border-green-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 transition-all"
          type="text"
          placeholder="Username"
          value={username}
          onChange={e => setUsername(e.target.value)}
          required
          autoComplete="username"
        />
      </div>
      <div className="mb-4">
        <label htmlFor="register-password" className="block mb-1 font-medium text-green-800">
          Password
        </label>
        <input
          id="register-password"
          name="password"
          className="block w-full p-3 border border-green-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 transition-all"
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          required
          autoComplete="new-password"
        />
      </div>
      <div className="mb-6">
        <label htmlFor="register-role" className="block mb-1 font-medium text-green-800">
          Role
        </label>
        <select
          id="register-role"
          name="role"
          className="block w-full p-3 border border-green-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 transition-all"
          value={role}
          onChange={e => setRole(e.target.value)}
        >
          <option value="patient">Patient</option>
          <option value="doctor">Doctor</option>
          <option value="admin">Admin</option>
        </select>
      </div>
      <button className="w-full bg-green-600 text-white py-2 rounded" type="submit">
        Register
      </button>
    </form>
  );
};

export default Register;