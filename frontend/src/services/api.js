import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const TaskService = {
  getTasks() {
    return apiClient.get('/tasks/');
  },

  getTask(id) {
    return apiClient.get(`/tasks/${id}/`);
  },

  createTask(task) {
    return apiClient.post('/tasks/', task);
  },

  updateTask(id, task) {
    return apiClient.put(`/tasks/${id}/`, task);
  },

  deleteTask(id) {
    return apiClient.delete(`/tasks/${id}/`);
  },
};

export const ThemeService = {
  getCurrentTheme() {
    return apiClient.get('/theme/');
  },

  updateTheme(theme) {
    return apiClient.put('/theme/', theme);
  },

  resetTheme() {
    return apiClient.delete('/theme/');
  },
}; 