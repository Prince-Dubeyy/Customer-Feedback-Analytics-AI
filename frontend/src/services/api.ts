import axios from 'axios';
import { API_BASE_URL } from '../config/api';

const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
});

export const uploadFeedback = async (file?: File, text?: string) => {
  const formData = new FormData();
  if (file) {
    formData.append('file', file);
  }
  if (text) {
    formData.append('text', text);
  }
  const response = await api.post('/upload-feedback', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const getDashboardStats = async () => {
  const response = await api.get('/dashboard');
  return response.data;
};

export const getMemories = async () => {
  const response = await api.get('/memory');
  return response.data;
};

export const getRoutingLogs = async () => {
  const response = await api.get('/routing-log');
  return response.data;
};

export const getReport = async () => {
  const response = await api.get('/report');
  return response.data;
};

export const getModelStats = async () => {
  const response = await api.get('/model-stats');
  return response.data;
};

export const resetData = async () => {
  const response = await api.post('/reset');
  return response.data;
};

export default api;
