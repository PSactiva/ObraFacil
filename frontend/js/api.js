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
  if (response.status === 204) return null;
  const data = await response.json();
  if (!response.ok) {
    const messages = Object.values(data).flat().join(' ');
    throw new Error(messages || `API error: ${response.status}`);
  }
  return data;
}

export async function login(username, password) {
  const data = await request('/auth/token/', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  });
  localStorage.setItem(TOKEN_KEY, data.token);
  return data;
}

export async function register(username, password, password_confirmation) {
  return request('/auth/register/', {
    method: 'POST',
    body: JSON.stringify({ username, password, password_confirmation }),
  });
}

export async function post(endpoint, data) {
  return request(endpoint, {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export async function patch(endpoint, data) {
  return request(endpoint, {
    method: 'PATCH',
    body: JSON.stringify(data),
  });
}

export async function remove(endpoint) {
  return request(endpoint, { method: 'DELETE' });
}

export async function get(endpoint) {
  return request(endpoint);
}

export function calcularArea(comprimento, largura) {
  return post('/calculos/area/', { comprimento, largura });
}

export function calcularConcreto(comprimento, largura, espessura) {
  return post('/calculos/concreto/', { comprimento, largura, espessura });
}

export function calcularPiso(comprimento, largura, perda_percentual) {
  return post('/calculos/piso/', { comprimento, largura, perda_percentual });
}

export function estimarCusto(area_m2, preco_unitario) {
  return post('/calculos/custo/', { area_m2, preco_unitario });
}
