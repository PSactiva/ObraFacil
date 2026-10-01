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
  const isFormData = options.body instanceof FormData;
  if (!isFormData) headers.set('Content-Type', 'application/json');
  const token = getToken();
  if (token) headers.set('Authorization', `Token ${token}`);

  const response = await fetch(`${API_BASE}${endpoint}`, { ...options, headers });
  if (response.status === 401) clearToken();
  if (response.status === 204) return null;
  let data = {};
  try {
    data = await response.json();
  } catch {
    // Respostas HTML ou vazias (por exemplo, erro 500 do servidor) não devem
    // esconder o status HTTP por trás de um erro de parse do JSON.
  }
  if (!response.ok) {
    const messages = Object.values(data).flat().filter((value) => typeof value === 'string').join(' ');
    const error = new Error(messages || `Erro HTTP ${response.status}`);
    error.status = response.status;
    throw error;
  }
  return data;
}

export async function login(username, password) {
  const data = await request('/auth/token/', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  });
  if (!data.token) {
    const error = new Error('A API não retornou um token de autenticação.');
    error.status = 502;
    throw error;
  }
  localStorage.setItem(TOKEN_KEY, data.token);
  return data;
}

export function getCurrentUser() {
  return request('/auth/me/');
}

export async function logout() {
  try {
    if (getToken()) await request('/auth/logout/', { method: 'POST' });
  } finally {
    clearToken();
  }
}

export function requestPasswordReset(email) {
  return request('/auth/password-reset/', {
    method: 'POST',
    body: JSON.stringify({ email }),
  });
}

export function confirmPasswordReset(uid, token, password, password_confirmation) {
  return request('/auth/password-reset/confirm/', {
    method: 'POST',
    body: JSON.stringify({ uid, token, password, password_confirmation }),
  });
}

export async function register(username, email, password, password_confirmation) {
  return request('/auth/register/', {
    method: 'POST',
    body: JSON.stringify({ username, email, password, password_confirmation }),
  });
}

export async function post(endpoint, data) {
  return request(endpoint, {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export async function postForm(endpoint, data) {
  return request(endpoint, { method: 'POST', body: data });
}

export async function patchForm(endpoint, data) {
  return request(endpoint, { method: 'PATCH', body: data });
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
