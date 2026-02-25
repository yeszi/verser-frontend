// src/config/api.js
const API_BASE_URL = 'https://verser-chain.vercel.app'  

export const API_ENDPOINTS = {
  LOGIN: `${API_BASE_URL}/login`,
  CERTIFICATES: `${API_BASE_URL}/issue-sertifikat`,
  VERIFY: (hash) => `${API_BASE_URL}/verify/${hash}`,
  HEALTH: `${API_BASE_URL}/`,
  CHAIN: `${API_BASE_URL}/chain`
}

export default API_BASE_URL