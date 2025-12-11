// src/lib/api.ts
import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE as string;

const api = axios.create({
  baseURL: API_BASE,
  timeout: 20000,
  headers: { 'Content-Type': 'application/json' },
});

export default api;
