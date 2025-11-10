import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export const apiService = {
  getDashboardAnalytics: () => api.get('/api/analytics/dashboard'),
  
  getNodes: () => api.get('/api/nodes'),
  getNode: (nodeId) => api.get(`/api/nodes/${nodeId}`),
  
  getSensorData: (nodeId, params = {}) => 
    api.get(`/api/sensor-data/${nodeId}`, { params }),
  
  getLatestData: () => api.get('/api/latest-data'),
  
  getRecommendations: (params = {}) => 
    api.get('/api/recommendations', { params }),
  
  getRecommendationsByNode: (nodeId, params = {}) => 
    api.get(`/api/recommendations/${nodeId}`, { params }),
  
  completeRecommendation: (recommendationId) => 
    api.post(`/api/recommendations/${recommendationId}/complete`),
  
  getAlerts: (params = {}) => 
    api.get('/api/alerts', { params }),
  
  acknowledgeAlert: (alertId) => 
    api.post(`/api/alerts/${alertId}/acknowledge`),
  
  getWeatherForecast: (location, days = 7) => 
    api.get(`/api/weather-forecast/${location}`, { params: { days } }),
  
  getTrends: (nodeId, days = 30) => 
    api.get(`/api/analytics/trends/${nodeId}`, { params: { days } }),
  
  registerCrop: (nodeId, cropData) => 
    api.post(`/api/crops/${nodeId}`, cropData),
  
  healthCheck: () => api.get('/api/health'),
  
  receiveSensorData: (data) => 
    api.post('/api/sensor-data', data),
};

export default api;
