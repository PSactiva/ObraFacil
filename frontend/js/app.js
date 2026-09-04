import { calcularArea, getToken, get, login, post } from './api.js';

const formArea = document.getElementById('form-area');
const resultadoArea = document.getElementById('resultado-area');
const offlineStatus = document.getElementById('offline-status');
const loginForm = document.getElementById('login-form');
const loginStatus = document.getElementById('login-status');
const orcamentoForm = document.getElementById('orcamento-form');
const orcamentosLista = document.getElementById('orcamentos-lista');

function updateOnlineStatus() {
  if (offlineStatus) {
    offlineStatus.textContent = navigator.onLine ? 'Conectado' : 'Modo offline — dados em cache';
  }
}

window.addEventListener('online', updateOnlineStatus);
window.addEventListener('offline', updateOnlineStatus);
updateOnlineStatus();

async function carregarOrcamentos() {
  if (!orcamentosLista || !getToken()) return;
  try {
    const data = await get('/orcamentos/');
    const orcamentos = data.results || data;
    orcamentosLista.innerHTML = orcamentos.length
      ? orcamentos.map((orcamento) => `
          <li class="border-b border-slate-200 py-3 last:border-0">
            <div class="flex justify-between gap-4">
              <strong>${orcamento.titulo}</strong>
              <span>R$ ${Number(orcamento.total).toFixed(2)}</span>
            </div>
            <small class="text-slate-500">${orcamento.cliente || 'Cliente não informado'}</small>
          </li>`).join('')
      : '<li class="text-slate-500">Nenhum orçamento cadastrado.</li>';
  } catch {
    orcamentosLista.innerHTML = '<li class="text-red-600">Não foi possível carregar os orçamentos.</li>';
  }
}

loginForm?.addEventListener('submit', async (event) => {
  event.preventDefault();
  const formData = new FormData(loginForm);
  loginStatus.textContent = 'Entrando...';
  try {
    await login(formData.get('username'), formData.get('password'));
    loginStatus.textContent = 'Login realizado.';
    orcamentoForm?.classList.remove('hidden');
    await carregarOrcamentos();
  } catch {
    loginStatus.textContent = 'Usuário ou senha inválidos.';
  }
});

orcamentoForm?.addEventListener('submit', async (event) => {
  event.preventDefault();
  const formData = new FormData(orcamentoForm);
  const status = document.getElementById('orcamento-status');
  status.textContent = 'Salvando...';
  try {
    await post('/orcamentos/', {
      titulo: formData.get('titulo'),
      cliente: formData.get('cliente'),
      descricao: formData.get('descricao'),
    });
    status.textContent = 'Orçamento salvo.';
    orcamentoForm.reset();
    await carregarOrcamentos();
  } catch {
    status.textContent = 'Não foi possível salvar. Faça login novamente.';
  }
});

if (getToken()) {
  orcamentoForm?.classList.remove('hidden');
  carregarOrcamentos();
}

if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/service-worker.js').catch(() => {});
}

formArea?.addEventListener('submit', async (event) => {
  event.preventDefault();
  const comprimento = parseFloat(document.getElementById('comprimento').value);
  const largura = parseFloat(document.getElementById('largura').value);
  resultadoArea.textContent = 'Calculando...';
  try {
    const data = await calcularArea(comprimento, largura);
    resultadoArea.textContent = `Área: ${data.area_m2.toFixed(2)} m²`;
  } catch {
    resultadoArea.textContent = `Área (local): ${(comprimento * largura).toFixed(2)} m²`;
  }
});
