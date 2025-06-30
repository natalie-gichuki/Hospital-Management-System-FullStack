const API_BASE_URL = 'http://127.0.0.1:5000/departments';

export const getDepartments = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/`);
    if (!response.ok) throw new Error('Failed to fetch departments');
    return await response.json();
  } catch (error) {
    console.error("Error fetching departments:", error);
    throw error;
  }
};

export const getDepartmentById = async (id) => {
  try {
    const response = await fetch(`${API_BASE_URL}/${id}`);
    if (!response.ok) throw new Error(`Failed to fetch department with ID ${id}`);
    return await response.json();
  } catch (error) {
    console.error(`Error fetching department with id ${id}:`, error);
    throw error;
  }
};

export const createDepartment = async (departmentData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(departmentData)
    });
    if (!response.ok) throw new Error('Failed to create department');
    return await response.json();
  } catch (error) {
    console.error("Error creating department:", error);
    throw error;
  }
};

export const updateDepartment = async (id, updatedData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updatedData)
    });
    if (!response.ok) throw new Error(`Failed to update department with ID ${id}`);
    return await response.json();
  } catch (error) {
    console.error(`Error updating department with id ${id}:`, error);
    throw error;
  }
};

export const deleteDepartment = async (id) => {
  try {
    const response = await fetch(`${API_BASE_URL}/${id}`, {
      method: 'DELETE'
    });
    if (!response.ok) throw new Error(`Failed to delete department with ID ${id}`);
    return true;
  } catch (error) {
    console.error(`Error deleting department with id ${id}:`, error);
    throw error;
  }
};
