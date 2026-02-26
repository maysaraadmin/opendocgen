import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

// API endpoints
export const apiService = {
  // Health check
  health: () => api.get('/health'),
  
  // Documents
  getDocuments: () => api.get('/api/v1/documents'),
  createDocument: (data: any) => api.post('/api/v1/documents', data),
  getDocument: (id: string) => api.get(`/api/v1/documents/${id}`),
  updateDocument: (id: string, data: any) => api.put(`/api/v1/documents/${id}`, data),
  deleteDocument: (id: string) => api.delete(`/api/v1/documents/${id}`),
  
  // Tasks
  getTasks: () => api.get('/api/v1/tasks'),
  createTask: (data: any) => api.post('/api/v1/tasks', data),
  getTask: (id: string) => api.get(`/api/v1/tasks/${id}`),
  updateTask: (id: string, data: any) => api.put(`/api/v1/tasks/${id}`, data),
  deleteTask: (id: string) => api.delete(`/api/v1/tasks/${id}`),
  
  // Files
  getFiles: () => api.get('/api/v1/files'),
  uploadFile: (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/api/v1/files/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  getFile: (id: string) => api.get(`/api/v1/files/${id}`),
  deleteFile: (id: string) => api.delete(`/api/v1/files/${id}`),
  
  // Agents
  getAgents: () => api.get('/api/v1/agents'),
  runAgent: (agentType: string, data: any) => api.post(`/api/v1/agents/${agentType}/run`, data),
};

export default api;
