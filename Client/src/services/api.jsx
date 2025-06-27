// Purpose: Defines the base URL for your backend API.
// import.meta.env.VITE_API_BASE_URL: Tries to load the value from your environment (e.g., .env file).
// Fallback: If nothing is defined, it defaults to 'http://127.0.0.1:5555'.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:5555';


// Sets default headers to send with every request.
// Content-Type: 'application/json' tells the server that you're sending JSON data.
// You can add more headers like authentication tokens later (e.g., Authorization: Bearer <token>).
const defaultHeaders = {
  'Content-Type': 'application/json',
  // You can also add Authorization headers here if needed
};


// You’re defining a reusable object api that will include helper methods like get, post, patch, and delete.
const api = {
  //   Takes endpoint as input, e.g., /appointments
  //   Uses fetch() to make a GET request to the full URL.
  //   headers: defaultHeaders attaches the Content-Type.
  //   If the response isn't OK (e.g., 404 or 500), it throws an error with the error message.
  //   Otherwise, it parses the JSON response and returns it.
  get: async (endpoint) => {
    const res = await fetch(`${API_BASE_URL}${endpoint}`, {
      headers: defaultHeaders,
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  //  Sends data to the server (e.g., to create a new record).
  // data is converted to a JSON string and included in the request body.
  // Throws an error if the response fails.
  // Returns the parsed JSON if successful.
  post: async (endpoint, data) => {
    const res = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'POST',
      headers: defaultHeaders,
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  patch: async (endpoint, data) => {
    const res = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'PATCH',
      headers: defaultHeaders,
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  delete: async (endpoint) => {
    const res = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'DELETE',
      headers: defaultHeaders,
    });
    if (!res.ok) throw new Error(await res.text());
    return res;
  },
};

export default api;


// The async keyword is used to declare a function that returns a Promise automatically. It makes the function asynchronous, allowing you to use await inside it.
// The await keyword pauses the execution of an async function until a Promise is resolved (or rejected).
// It lets you write asynchronous code in a way that looks and reads like synchronous code, avoiding .then() chains.