// services/api.jsx
// Removed: import { getToken } from './AuthService'; // <--- REMOVED THIS IMPORT

// Purpose: Defines the base URL for your backend API.
const API_BASE_URL = 'http://127.0.0.1:5000'; // Make sure this matches your Flask backend URL

// Sets default headers to send with every request.
// It no longer dynamically adds the Authorization header as JWT is removed.
const getAuthHeaders = () => {
  // Removed: const token = getToken();
  // Removed: return token ? { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` } : { 'Content-Type': 'application/json' };
  return { 'Content-Type': 'application/json' }; // <--- SIMPLIFIED: Only Content-Type is sent
};

// You’re defining a reusable object api that will include helper methods like get, post, patch, and delete.
const api = {
  get: async (endpoint) => {
    const res = await fetch(`${API_BASE_URL}${endpoint}`, {
      headers: getAuthHeaders(),
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  post: async (endpoint, data) => {
    const res = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  patch: async (endpoint, data) => {
    const res = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'PATCH',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  delete: async (endpoint) => {
    const res = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'DELETE',
      headers: getAuthHeaders(),
    });
    // For DELETE, a 204 No Content response is common for success
    if (!res.ok && res.status !== 204) throw new Error(await res.text());
    return true; // Indicate success for deletion
  },
};

export default api;