// Import the axios HTTP client library
import axios from 'axios';

// Set the base URL for API requests.
// It tries to use a value from the .env file (VITE_API_BASE_URL), 
// and falls back to 'http://127.0.0.1:5555' if not provided.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:5555/patients';

// Create an axios instance with default settings.
// This instance can be reused across your app for all API calls.
const api = axios.create({
  baseURL: API_BASE_URL, // All requests made with this instance will prepend this base URL
  headers: {
    'Content-Type': 'application/json', // Ensure the server expects and receives JSON
  },
});

// Export the configured axios instance so it can be imported in other files
export default api;
