// services/api.jsx
// No need to import useNavigate here unless you want to implement
// automatic redirection on 401/403, which is usually handled by App.jsx

// Purpose: Defines the base URL for your backend API.
const API_BASE_URL = 'http://127.0.0.1:5000'; // Make sure this matches your Flask backend URL

// Sets default headers to send with every request.
const getAuthHeaders = () => {
  return { 'Content-Type': 'application/json' };
};

const api = {
  // Centralized request method to handle common logic for all HTTP methods
  request: async (endpoint, options = {}) => {
    const defaultOptions = {
      headers: getAuthHeaders(),
      ...options, // Spread in any method-specific options (e.g., method: 'POST', body: JSON.stringify(data))
    };

    const res = await fetch(`${API_BASE_URL}${endpoint}`, defaultOptions);

    if (!res.ok) { // If the response status is not in the 200-299 range
      let errorData;
      // Try to parse the response body as JSON.
      // This is crucial because your backend might send JSON even for error responses.
      try {
        errorData = await res.json();
      } catch (e) {
        // If parsing as JSON fails (e.g., plain text error, HTML error page), get it as text
        errorData = await res.text();
      }

      // Construct a more informative error message
      let errorMessage = `Request failed: Status ${res.status}`;
      if (typeof errorData === 'object' && errorData !== null) {
        // If the error data is a JSON object, try to extract 'message' or 'error' fields
        errorMessage = errorData.message || errorData.error || JSON.stringify(errorData);
      } else if (typeof errorData === 'string' && errorData.trim() !== '') {
        // If it's a non-empty plain text string
        errorMessage = errorData;
      } else if (res.statusText) {
        // Fallback to status text if no meaningful body
        errorMessage = res.statusText;
      }

      // Re-throw the error with the more informative message
      throw new Error(errorMessage);
    }

    // For successful responses (res.ok is true):
    // If it's a 204 No Content response (common for successful DELETE), return true or null
    if (res.status === 204) {
      return true; // Indicates success for operations that return no content
    }

    // Otherwise, parse and return the JSON response
    return res.json();
  },

  get: async (endpoint) => api.request(endpoint, { method: 'GET' }),
  post: async (endpoint, data) => api.request(endpoint, { method: 'POST', body: JSON.stringify(data) }),
  patch: async (endpoint, data) => api.request(endpoint, { method: 'PATCH', body: JSON.stringify(data) }),
  delete: async (endpoint) => api.request(endpoint, { method: 'DELETE' }),
};

export default api;