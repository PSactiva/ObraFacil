const API_BASE = '/api';

const TOKEN_KEY = 'obrafacil_api_token';

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
}

async function request(endpoint, options = {}) {
  const headers = new Headers(options.headers || {});
  headers.set('Content-Type', 'application/json');
  const token = getToken();
  if (token) headers.set('Authorization', `Token ${token}`);

  const response = await fetch(`${API_BASE}${endpoint}`, { ...options, headers });
  if (!response.ok) throw new Error(`API error: ${response.status}`);
  if (response.status === 204) return null;
  return response.json();
}

export async function login(username, password) {
  const data = await request('/auth/token/', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  });
  localStorage.setItem(TOKEN_KEY, data.token);
  return data;
}

export async function post(endpoint, data) {
  return request(endpoint, {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export async function get(endpoint) {
  return request(endpoint);
}

export function calcularArea(comprimento, largura) {
  return post('/calculos/area/', { comprimento, largura });
}
