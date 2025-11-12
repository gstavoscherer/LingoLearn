// Server-side API configuration
// Use internal Docker network URL for server-side requests
export const API_URL = import.meta.env.VITE_API_URL ?? 'http://backend:5000';
