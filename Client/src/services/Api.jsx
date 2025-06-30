const API_BASE_URL = 'http://127.0.0.1:5000';

const getAuthHeaders = () => ({ 'Content-Type': 'application/json' });

const api = {
  request: async (endpoint, options = {}) => {
    const defaultOptions = {
      headers: getAuthHeaders(),
      ...options,
    };

    const res = await fetch(`${API_BASE_URL}${endpoint}`, defaultOptions);

    if (!res.ok) {
      let errorData;
      try {
        errorData = await res.json();
      } catch (error) { // changed from (e) to (_) to indicate unused variable
        errorData = await res.text(error);
      }

      let errorMessage = `Request failed: Status ${res.status}`;
      if (typeof errorData === 'object' && errorData !== null) {
        errorMessage = errorData.message || errorData.error || JSON.stringify(errorData);
      } else if (typeof errorData === 'string' && errorData.trim() !== '') {
        errorMessage = errorData;
      } else if (res.statusText) {
        errorMessage = res.statusText;
      }

      throw new Error(errorMessage);
    }

    if (res.status === 204) return true;
    return res.json();
  },

  get: (endpoint) => api.request(endpoint, { method: 'GET' }),
  post: (endpoint, data) => api.request(endpoint, { method: 'POST', body: JSON.stringify(data) }),
  patch: (endpoint, data) => api.request(endpoint, { method: 'PATCH', body: JSON.stringify(data) }),
  delete: (endpoint) => api.request(endpoint, { method: 'DELETE' }),
};

export default api;