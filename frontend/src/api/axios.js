import axios from 'axios';

const api = axios.create({
    baseURL: '/api' // Relies on Vite proxy
});

export default api;
