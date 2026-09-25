import {
  calcularArea,
  calcularConcreto,
  calcularPiso,
  estimarCusto,
  getToken,
  getCurrentUser,
  get,
  login,
  logout,
  requestPasswordReset,
  confirmPasswordReset,
  patch,
  post,
  register,
  remove,
} from './api.js';

const formArea = document.getElementById('form-area');
const resultadoArea = document.getElementById('resultado-area');
const offlineStatus = document.getElementById('offline-status');
const loginForm = document.getElementById('login-form');
const loginStatus = document.getElementById('login-status');
const registerForm = document.getElementById('register-form');
const registerStatus = document.getElementById('register-status');
const passwordResetRequestForm = document.getElementById('password-reset-request-form');
const passwordResetRequestStatus = document.getElementById('password-reset-request-status');
const passwordResetConfirmForm = document.getElementById('password-reset-confirm-form');
const passwordResetConfirmStatus = document.getElementById('password-reset-confirm-status');
const sessionPanel = document.getElementById('session-panel');
const sessionUsername = document.getElementById('session-username');
const logoutButton = document.getElementById('logout-button');
const orcamentoForm = document.getElementById('orcamento-form');
const orcamentosLista = document.getElementById('orcamentos-lista');
const itensContainer = document.getElementById('orcamento-itens');
const itensVazio = document.getElementById('itens-vazio');
const adicionarItemButton = document.getElementById('adicionar-item');
const formTitulo = document.getElementById('orcamento-form-titulo');
const cancelarEdicaoButton = document.getElementById('cancelar-edicao');
const materiaisLista = document.getElementById('materiais-lista');
const buscaMaterial = document.getElementById('buscar-material');
const materialForm = document.getElementById('material-form');
const materialFormTitulo = document.getElementById('material-form-titulo');
const cancelarMaterialButton = document.getElementById('cancelar-material');
const materialStatus = document.getElementById('material-status');
const obraForm = document.getElementById('obra-form');
const obraFormTitulo = document.getElementById('obra-form-titulo');
const cancelarObraButton = document.getElementById('cancelar-obra');
const obraStatusMsg = document.getElementById('obra-status-msg');
const obrasLista = document.getElementById('obras-lista');
const funcionarioForm = document.getElementById('funcionario-form');
const funcionarioFormTitulo = document.getElementById('funcionario-form-titulo');
const funcionarioStatus = document.getElementById('funcionario-status-msg');
const funcionariosLista = document.getElementById('funcionarios-lista');
const novoFuncionarioButton = document.getElementById('novo-funcionario');
const cancelarFuncionarioButton = document.getElementById('cancelar-funcionario');
const presencaForm = document.getElementById('presenca-form');
const presencaFuncionarioSelect = document.getElementById('presenca-funcionario');
const presencaObraSelect = document.getElementById('presenca-obra');
const presencaStatus = document.getElementById('presenca-status');
const presencasLista = document.getElementById('presencas-lista');
const registrarPresencaButton = document.getElementById('registrar-presenca');

let materiais = [];
let orcamentoEmEdicao = null;
let materialEmEdicao = null;
let obraEmEdicao = null;
let funcionarioEmEdicao = null;

function formatarMoeda(valor) {
  return Number(valor).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
}

function escaparHtml(valor) {
  return String(valor).replace(/[&<>'"]/g, (caractere) => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    "'": '&#39;',
    '"': '&quot;',
  }[caractere]));
}

function renderizarMateriais(filtro = '') {
  if (!materiaisLista) return;
  const termo = filtro.trim().toLocaleLowerCase('pt-BR');
  const filtrados = materiais.filter((material) =>
    `${material.nome} ${material.categoria}`.toLocaleLowerCase('pt-BR').includes(termo)
  );
  materiaisLista.innerHTML = filtrados.length
    ? filtrados.map((material) => `
        <tr data-material-id="${material.id}">
          <td class="py-3 px-4 font-semibold">${escaparHtml(material.nome)}</td>
          <td class="py-3 px-4">${escaparHtml(material.categoria || 'Sem categoria')}</td>
          <td class="py-3 px-4">${escaparHtml(material.unidade)}</td>
          <td class="py-3 px-4">${formatarMoeda(material.preco_unitario)}</td>
          <td class="py-3 px-4">${getToken() ? `<button type="button" data-material-acao="editar" class="mr-2 text-sm font-semibold text-slate-700 hover:underline">Editar</button><button type="button" data-material-acao="excluir" class="text-sm font-semibold text-red-700 hover:underline">Excluir</button>` : '<span class="text-sm text-slate-400">Somente consulta</span>'}</td>
        </tr>`).join('')
    : '<tr><td colspan="5" class="py-4 px-4 text-slate-500">Nenhum material encontrado.</td></tr>';
}

function atualizarResumoDoItem(linha) {
  const materialId = Number(linha.querySelector('[name="material"]').value);
  const quantidade = Number(linha.querySelector('[name="quantidade"]').value || 0);
  const material = materiais.find((item) => item.id === materialId);
  const preco = material ? Number(material.preco_unitario) : 0;
  const resumo = linha.querySelector('.resumo-item');
  if (resumo) {
    resumo.textContent = material
      ? `${formatarMoeda(preco)} por ${material.unidade} | Subtotal: ${formatarMoeda(preco * quantidade)}`
      : 'Selecione um material';
  }
}

function atualizarEstadoDosItens() {
  if (itensVazio) itensVazio.classList.toggle('hidden', Boolean(itensContainer?.children.length));
}

function criarLinhaDeItem(materialSelecionado = null, quantidade = '') {
  if (!itensContainer) return;
  const linha = document.createElement('div');
  linha.className = 'grid grid-cols-1 gap-2 rounded-lg border border-slate-200 p-3 md:grid-cols-[minmax(0,1fr)_9rem_auto]';
  linha.innerHTML = `
    <label class="sr-only">Material</label>
    <select name="material" required class="material-select rounded-lg border border-slate-300 px-3 py-2">
      <option value="">Selecione um material</option>
      ${materiais.map((material) => `<option value="${material.id}" data-preco="${material.preco_unitario}">${escaparHtml(material.nome)} (${escaparHtml(material.unidade)}) - ${formatarMoeda(material.preco_unitario)}</option>`).join('')}
    </select>
    <label class="sr-only">Quantidade</label>
    <input name="quantidade" required min="0.001" step="0.001" type="number" placeholder="Quantidade" class="rounded-lg border border-slate-300 px-3 py-2">
    <button type="button" class="remover-item rounded-lg border border-red-200 px-3 py-2 text-sm font-semibold text-red-700 hover:bg-red-50">Remover</button>
    <p class="resumo-item text-xs text-slate-500 md:col-span-3">Selecione um material</p>
  `;
  if (materialSelecionado !== null) {
    linha.querySelector('[name="material"]').value = materialSelecionado;
    linha.querySelector('[name="quantidade"]').value = quantidade;
  }
  linha.querySelector('.remover-item').addEventListener('click', () => {
    linha.remove();
    atualizarEstadoDosItens();
  });
  linha.querySelector('[name="material"]').addEventListener('change', () => atualizarResumoDoItem(linha));
  linha.querySelector('[name="quantidade"]').addEventListener('input', () => atualizarResumoDoItem(linha));
  itensContainer.appendChild(linha);
  atualizarResumoDoItem(linha);
  atualizarEstadoDosItens();
}

async function carregarMateriais() {
  try {
    const data = await get('/materiais/');
    materiais = data.results || data;
    if (adicionarItemButton) {
      adicionarItemButton.disabled = !materiais.length;
      adicionarItemButton.title = materiais.length ? '' : 'Cadastre materiais antes de criar um orçamento.';
    }
    if (!materiais.length && itensVazio) itensVazio.textContent = 'Nenhum material ativo cadastrado.';
    renderizarMateriais(buscaMaterial?.value || '');
  } catch {
    if (adicionarItemButton) adicionarItemButton.disabled = true;
    if (itensVazio) itensVazio.textContent = 'Não foi possível carregar os materiais.';
    if (materiaisLista) materiaisLista.innerHTML = '<tr><td colspan="5" class="py-4 px-4 text-red-600">Não foi possível carregar os materiais.</td></tr>';
  }
}

function limparFormularioMaterial() {
  materialForm?.reset();
  materialEmEdicao = null;
  if (materialFormTitulo) materialFormTitulo.textContent = 'Novo material';
  cancelarMaterialButton?.classList.add('hidden');
}

function preencherFormularioMaterial(material) {
  materialForm?.classList.remove('hidden');
  materialEmEdicao = material.id;
  document.getElementById('material-nome').value = material.nome;
  document.getElementById('material-categoria').value = material.categoria || '';
  document.getElementById('material-unidade').value = material.unidade;
  document.getElementById('material-preco').value = material.preco_unitario;
  if (materialFormTitulo) materialFormTitulo.textContent = 'Editar material';
  cancelarMaterialButton?.classList.remove('hidden');
  materialForm?.scrollIntoView({ behavior: 'smooth' });
}

function formatarData(data) {
  if (!data) return 'Sem data definida';
  return new Date(`${data}T00:00:00`).toLocaleDateString('pt-BR');
}

function classeStatusObra(status) {
  return {
    planejada: 'bg-slate-100 text-slate-700',
    em_andamento: 'bg-amber-100 text-amber-800',
    concluida: 'bg-emerald-100 text-emerald-800',
    pausada: 'bg-red-100 text-red-800',
  }[status] || 'bg-slate-100 text-slate-700';
}

function renderizarObras(obras) {
  if (!obrasLista) return;
  obrasLista.innerHTML = obras.length
    ? obras.map((obra) => `
        <tr data-obra-id="${obra.id}">
          <td class="py-3 px-4 font-semibold">${escaparHtml(obra.nome)}<small class="block text-xs font-normal text-slate-500">${escaparHtml(obra.endereco || 'Endereço não informado')}</small></td>
          <td class="py-3 px-4">${escaparHtml(obra.cliente)}</td>
          <td class="py-3 px-4 text-sm">${formatarData(obra.data_inicio)}<small class="block text-xs text-slate-500">até ${formatarData(obra.previsao_conclusao)}</small></td>
          <td class="py-3 px-4"><span class="rounded px-2 py-1 text-xs ${classeStatusObra(obra.status)}">${escaparHtml(obra.status_display)}</span></td>
          <td class="py-3 px-4">${getToken() ? `<button type="button" data-obra-acao="editar" class="mr-2 text-sm font-semibold text-slate-700 hover:underline">Editar</button><button type="button" data-obra-acao="excluir" class="text-sm font-semibold text-red-700 hover:underline">Excluir</button>` : '<span class="text-sm text-slate-400">Somente consulta</span>'}</td>
        </tr>`).join('')
    : '<tr><td colspan="5" class="py-4 px-4 text-slate-500">Nenhuma obra cadastrada.</td></tr>';
}

async function carregarObras() {
  try {
    const data = await get('/obras/');
    renderizarObras(data.results || data);
  } catch {
    if (obrasLista) obrasLista.innerHTML = '<tr><td colspan="5" class="py-4 px-4 text-red-600">Não foi possível carregar as obras.</td></tr>';
  }
}

function renderizarFuncionarios(funcionarios) {
  if (!funcionariosLista) return;
  funcionariosLista.innerHTML = funcionarios.length
    ? funcionarios.map((funcionario) => `
        <tr data-funcionario-id="${funcionario.id}">
          <td class="py-3 px-4 font-semibold">${escaparHtml(funcionario.nome)}</td>
          <td class="py-3 px-4">${escaparHtml(funcionario.cargo)}</td>
          <td class="py-3 px-4 text-sm">${escaparHtml(funcionario.email || 'Sem e-mail')}<small class="block text-xs text-slate-500">${escaparHtml(funcionario.telefone || 'Sem telefone')}</small></td>
          <td class="py-3 px-4"><span class="rounded px-2 py-1 text-xs ${funcionario.ativo ? 'bg-emerald-100 text-emerald-800' : 'bg-slate-100 text-slate-700'}">${funcionario.ativo ? 'Ativo' : 'Inativo'}</span></td>
          <td class="py-3 px-4"><button type="button" data-funcionario-acao="editar" class="mr-2 text-sm font-semibold text-slate-700 hover:underline">Editar</button><button type="button" data-funcionario-acao="excluir" class="text-sm font-semibold text-red-700 hover:underline">Excluir</button></td>
        </tr>`).join('')
    : '<tr><td colspan="5" class="py-4 px-4 text-slate-500">Nenhum funcionário cadastrado.</td></tr>';
}

async function carregarFuncionarios() {
  if (!funcionariosLista || !getToken()) return;
  funcionariosLista.innerHTML = '<tr><td colspan="5" class="py-4 px-4 text-slate-500">Carregando funcionários...</td></tr>';
  try {
    const data = await get('/funcionarios/');
    renderizarFuncionarios(data.results || data);
  } catch (error) {
    funcionariosLista.innerHTML = `<tr><td colspan="5" class="py-4 px-4 text-red-600">${escaparHtml(error.message || 'Não foi possível carregar os funcionários.')}</td></tr>`;
  }
}

function formatarDataHora(dataHora) {
  return new Date(dataHora).toLocaleString('pt-BR', {
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit',
  });
}

async function carregarPresencas() {
  if (!presencasLista || !getToken()) return;
  presencasLista.innerHTML = '<tr><td colspan="4" class="py-4 px-4 text-slate-500">Carregando presenças...</td></tr>';
  try {
    const [presencasData, funcionariosData, obrasData] = await Promise.all([
      get('/presencas/'),
      get('/funcionarios/'),
      get('/obras/'),
    ]);
    const presencas = presencasData.results || presencasData;
    const funcionarios = (funcionariosData.results || funcionariosData).filter((funcionario) => funcionario.ativo);
    const obras = obrasData.results || obrasData;
    const funcionariosComPresenca = new Set(presencas.map((presenca) => presenca.funcionario));

    if (presencaFuncionarioSelect) {
      presencaFuncionarioSelect.innerHTML = '<option value="">Selecione um funcionário</option>' + funcionarios.map((funcionario) => `
        <option value="${funcionario.id}" ${funcionariosComPresenca.has(funcionario.id) ? 'disabled' : ''}>${escaparHtml(funcionario.nome)}${funcionariosComPresenca.has(funcionario.id) ? ' (presença registrada)' : ''}</option>`).join('');
    }
    if (presencaObraSelect) {
      presencaObraSelect.innerHTML = '<option value="">Sem obra vinculada</option>' + obras.map((obra) => `
        <option value="${obra.id}">${escaparHtml(obra.nome)}</option>`).join('');
    }
    if (registrarPresencaButton) registrarPresencaButton.disabled = !funcionarios.some((funcionario) => !funcionariosComPresenca.has(funcionario.id));

    presencasLista.innerHTML = presencas.length
      ? presencas.map((presenca) => `
          <tr>
            <td class="py-3 px-4"><span class="font-semibold">${escaparHtml(presenca.funcionario_nome)}</span><small class="block text-xs text-slate-500">${escaparHtml(presenca.funcionario_cargo)}</small></td>
            <td class="py-3 px-4">${escaparHtml(presenca.obra_nome || 'Sem obra vinculada')}</td>
            <td class="py-3 px-4">${formatarData(presenca.data)}</td>
            <td class="py-3 px-4">${formatarDataHora(presenca.registrado_em)}</td>
          </tr>`).join('')
      : '<tr><td colspan="4" class="py-4 px-4 text-slate-500">Nenhuma presença registrada hoje.</td></tr>';
    if (presencaStatus) {
      presencaStatus.textContent = funcionarios.length
        ? 'Selecione um funcionário ativo para registrar a presença de hoje.'
        : 'Cadastre um funcionário ativo antes de registrar presença.';
    }
  } catch (error) {
    presencasLista.innerHTML = `<tr><td colspan="4" class="py-4 px-4 text-red-600">${escaparHtml(error.message || 'Não foi possível carregar as presenças.')}</td></tr>`;
    if (presencaStatus) presencaStatus.textContent = 'Não foi possível carregar os dados necessários para registrar presença.';
  }
}

function limparFormularioFuncionario() {
  funcionarioForm?.reset();
  funcionarioEmEdicao = null;
  funcionarioForm?.classList.add('hidden');
  if (funcionarioFormTitulo) funcionarioFormTitulo.textContent = 'Novo funcionário';
  if (funcionarioStatus) funcionarioStatus.textContent = '';
  cancelarFuncionarioButton?.classList.add('hidden');
}

function preencherFormularioFuncionario(funcionario) {
  funcionarioForm?.classList.remove('hidden');
  funcionarioEmEdicao = funcionario.id;
  document.getElementById('funcionario-nome').value = funcionario.nome;
  document.getElementById('funcionario-cargo').value = funcionario.cargo;
  document.getElementById('funcionario-email').value = funcionario.email || '';
  document.getElementById('funcionario-telefone').value = funcionario.telefone || '';
  document.getElementById('funcionario-ativo').checked = funcionario.ativo;
  if (funcionarioFormTitulo) funcionarioFormTitulo.textContent = 'Editar funcionário';
  cancelarFuncionarioButton?.classList.remove('hidden');
  funcionarioForm?.scrollIntoView({ behavior: 'smooth' });
}

function limparFormularioObra() {
  obraForm?.reset();
  obraEmEdicao = null;
  if (obraFormTitulo) obraFormTitulo.textContent = 'Nova obra';
  cancelarObraButton?.classList.add('hidden');
  if (obraStatusMsg) obraStatusMsg.textContent = '';
}

function preencherFormularioObra(obra) {
  obraForm?.classList.remove('hidden');
  obraEmEdicao = obra.id;
  document.getElementById('obra-nome').value = obra.nome;
  document.getElementById('obra-cliente').value = obra.cliente;
  document.getElementById('obra-endereco').value = obra.endereco || '';
  document.getElementById('obra-status').value = obra.status;
  document.getElementById('obra-data-inicio').value = obra.data_inicio || '';
  document.getElementById('obra-previsao').value = obra.previsao_conclusao || '';
  if (obraFormTitulo) obraFormTitulo.textContent = 'Editar obra';
  cancelarObraButton?.classList.remove('hidden');
  obraForm?.scrollIntoView({ behavior: 'smooth' });
}

function coletarItens() {
  return [...(itensContainer?.querySelectorAll('.grid') || [])].map((linha) => ({
    material: Number(linha.querySelector('[name="material"]').value),
    quantidade: linha.querySelector('[name="quantidade"]').value,
  }));
}

function limparFormulario() {
  orcamentoForm?.reset();
  if (itensContainer) itensContainer.innerHTML = '';
  atualizarEstadoDosItens();
  orcamentoEmEdicao = null;
  if (formTitulo) formTitulo.textContent = 'Novo orçamento';
  if (cancelarEdicaoButton) cancelarEdicaoButton.classList.add('hidden');
}

function preencherFormulario(orcamento) {
  if (!orcamentoForm) return;
  orcamentoEmEdicao = orcamento.id;
  document.getElementById('orcamento-titulo').value = orcamento.titulo;
  document.getElementById('orcamento-cliente').value = orcamento.cliente || '';
  document.getElementById('orcamento-descricao').value = orcamento.descricao || '';
  if (itensContainer) itensContainer.innerHTML = '';
  (orcamento.itens || []).forEach((item) => {
    criarLinhaDeItem(item.material, item.quantidade);
  });
  atualizarEstadoDosItens();
  if (formTitulo) formTitulo.textContent = 'Editar orçamento';
  if (cancelarEdicaoButton) cancelarEdicaoButton.classList.remove('hidden');
  orcamentoForm.classList.remove('hidden');
  orcamentoForm.scrollIntoView({ behavior: 'smooth' });
}

function updateOnlineStatus() {
  if (offlineStatus) {
    offlineStatus.textContent = navigator.onLine ? 'Conectado' : 'Modo offline — dados em cache';
  }
}

function atualizarEstadoDaSessao(usuario = null) {
  const autenticado = Boolean(usuario);
  loginForm?.classList.toggle('hidden', autenticado);
  registerForm?.classList.toggle('hidden', autenticado);
  sessionPanel?.classList.toggle('hidden', !autenticado);
  if (sessionUsername) sessionUsername.textContent = usuario?.username || '';
  orcamentoForm?.classList.toggle('hidden', !autenticado);
  materialForm?.classList.toggle('hidden', !autenticado);
  obraForm?.classList.toggle('hidden', !autenticado);
  novoFuncionarioButton?.classList.toggle('hidden', !autenticado);
  presencaForm?.classList.toggle('hidden', !autenticado);
  if (!autenticado) {
    limparFormularioFuncionario();
    if (funcionariosLista) funcionariosLista.innerHTML = '<tr><td colspan="5" class="py-4 px-4 text-slate-500">Faça login para carregar os funcionários.</td></tr>';
    if (presencasLista) presencasLista.innerHTML = '<tr><td colspan="4" class="py-4 px-4 text-slate-500">Faça login para carregar as presenças.</td></tr>';
    if (presencaStatus) presencaStatus.textContent = 'Faça login para registrar e consultar presenças.';
  }
}

async function carregarDadosAutenticados() {
  await carregarMateriais();
  await carregarObras();
  await carregarOrcamentos();
  await carregarFuncionarios();
  await carregarPresencas();
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
          <li class="border-b border-slate-200 py-4 last:border-0" data-orcamento-id="${orcamento.id}">
            <div class="flex flex-wrap items-start justify-between gap-3">
              <div>
                <strong class="text-slate-800">${escaparHtml(orcamento.titulo)}</strong>
                <p class="text-sm text-slate-500">${escaparHtml(orcamento.cliente || 'Cliente não informado')}</p>
              </div>
              <strong class="text-slate-900">${formatarMoeda(orcamento.total)}</strong>
            </div>
            <ul class="mt-2 space-y-1 text-sm text-slate-600">
              ${(orcamento.itens || []).map((item) => `<li>${escaparHtml(item.material_nome)}: ${item.quantidade} x ${formatarMoeda(item.preco_unitario)} = ${formatarMoeda(item.subtotal)}</li>`).join('') || '<li>Nenhum item informado.</li>'}
            </ul>
            <div class="mt-3 flex gap-2">
              <button type="button" data-acao="editar" class="rounded-lg border border-slate-300 px-3 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50">Editar</button>
              <button type="button" data-acao="excluir" class="rounded-lg border border-red-200 px-3 py-2 text-sm font-semibold text-red-700 hover:bg-red-50">Excluir</button>
            </div>
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
    const usuario = await getCurrentUser();
    loginStatus.textContent = 'Login realizado.';
    atualizarEstadoDaSessao(usuario);
    await carregarDadosAutenticados();
  } catch {
    loginStatus.textContent = 'Usuário ou senha inválidos.';
  }
});

registerForm?.addEventListener('submit', async (event) => {
  event.preventDefault();
  const formData = new FormData(registerForm);
  registerStatus.textContent = 'Cadastrando...';
  try {
    await register(
      formData.get('username'),
      formData.get('email'),
      formData.get('password'),
      formData.get('password_confirmation'),
    );
    await login(formData.get('username'), formData.get('password'));
    const usuario = await getCurrentUser();
    registerStatus.textContent = 'Usuário cadastrado e conectado.';
    registerForm.reset();
    atualizarEstadoDaSessao(usuario);
    await carregarDadosAutenticados();
  } catch (error) {
    registerStatus.textContent = error.message || 'Não foi possível conectar ao servidor.';
  }
});

passwordResetRequestForm?.addEventListener('submit', async (event) => {
  event.preventDefault();
  passwordResetRequestStatus.textContent = 'Enviando...';
  try {
    await requestPasswordReset(new FormData(passwordResetRequestForm).get('email'));
    passwordResetRequestStatus.textContent = 'Se o e-mail estiver cadastrado, as instruções foram enviadas.';
    passwordResetRequestForm.reset();
  } catch {
    passwordResetRequestStatus.textContent = 'Não foi possível solicitar a recuperação agora.';
  }
});

passwordResetConfirmForm?.addEventListener('submit', async (event) => {
  event.preventDefault();
  const parametros = new URLSearchParams(window.location.search);
  const formData = new FormData(passwordResetConfirmForm);
  passwordResetConfirmStatus.textContent = 'Redefinindo...';
  try {
    await confirmPasswordReset(
      parametros.get('uid'),
      parametros.get('token'),
      formData.get('password'),
      formData.get('password_confirmation'),
    );
    passwordResetConfirmStatus.textContent = 'Senha redefinida. Você já pode entrar.';
    passwordResetConfirmForm.reset();
    window.history.replaceState({}, document.title, window.location.pathname);
  } catch (error) {
    passwordResetConfirmStatus.textContent = error.message || 'Link inválido ou expirado.';
  }
});

orcamentoForm?.addEventListener('submit', async (event) => {
  event.preventDefault();
  const formData = new FormData(orcamentoForm);
  const status = document.getElementById('orcamento-status');
  status.textContent = 'Salvando...';
  try {
    const itens = coletarItens();
    if (!itens.length) {
      status.textContent = 'Adicione pelo menos um material.';
      return;
    }
    const dados = {
      titulo: formData.get('titulo'),
      cliente: formData.get('cliente'),
      descricao: formData.get('descricao'),
      itens,
    };
    if (orcamentoEmEdicao) {
      await patch(`/orcamentos/${orcamentoEmEdicao}/`, dados);
      status.textContent = 'Orçamento atualizado.';
    } else {
      await post('/orcamentos/', dados);
      status.textContent = 'Orçamento salvo.';
    }
    limparFormulario();
    await carregarOrcamentos();
  } catch {
    status.textContent = 'Não foi possível salvar. Faça login novamente.';
  }
});

logoutButton?.addEventListener('click', async () => {
  logoutButton.disabled = true;
  try {
    await logout();
  } finally {
    atualizarEstadoDaSessao();
    orcamentosLista && (orcamentosLista.innerHTML = '<li class="text-slate-500">Faça login para carregar os orçamentos.</li>');
    loginStatus.textContent = 'Sessão encerrada.';
    logoutButton.disabled = false;
  }
});

async function iniciarAutenticacao() {
  const parametros = new URLSearchParams(window.location.search);
  if (parametros.has('uid') && parametros.has('token')) {
    passwordResetConfirmForm?.classList.remove('hidden');
  }
  if (!getToken()) {
    atualizarEstadoDaSessao();
    return;
  }
  try {
    const usuario = await getCurrentUser();
    atualizarEstadoDaSessao(usuario);
    await carregarDadosAutenticados();
  } catch {
    atualizarEstadoDaSessao();
  }
}

iniciarAutenticacao();

carregarMateriais();
carregarObras();
adicionarItemButton?.addEventListener('click', criarLinhaDeItem);
buscaMaterial?.addEventListener('input', () => renderizarMateriais(buscaMaterial.value));

materialForm?.addEventListener('submit', async (event) => {
  event.preventDefault();
  const dados = Object.fromEntries(new FormData(materialForm).entries());
  dados.preco_unitario = Number(dados.preco_unitario).toFixed(2);
  materialStatus.textContent = 'Salvando...';
  try {
    if (materialEmEdicao) {
      await patch(`/materiais/${materialEmEdicao}/`, dados);
      materialStatus.textContent = 'Material atualizado.';
    } else {
      await post('/materiais/', { ...dados, ativo: true });
      materialStatus.textContent = 'Material cadastrado.';
    }
    limparFormularioMaterial();
    await carregarMateriais();
  } catch {
    materialStatus.textContent = 'Não foi possível salvar. Faça login novamente.';
  }
});

cancelarMaterialButton?.addEventListener('click', limparFormularioMaterial);

obraForm?.addEventListener('submit', async (event) => {
  event.preventDefault();
  const dados = Object.fromEntries(new FormData(obraForm).entries());
  Object.keys(dados).forEach((campo) => {
    if (dados[campo] === '') delete dados[campo];
  });
  obraStatusMsg.textContent = 'Salvando...';
  try {
    if (obraEmEdicao) {
      await patch(`/obras/${obraEmEdicao}/`, dados);
      obraStatusMsg.textContent = 'Obra atualizada.';
    } else {
      await post('/obras/', dados);
      obraStatusMsg.textContent = 'Obra cadastrada.';
    }
    limparFormularioObra();
    await carregarObras();
  } catch (error) {
    obraStatusMsg.textContent = error.message || 'Não foi possível salvar a obra.';
  }
});

cancelarObraButton?.addEventListener('click', limparFormularioObra);

novoFuncionarioButton?.addEventListener('click', () => {
  limparFormularioFuncionario();
  funcionarioForm?.classList.remove('hidden');
  funcionarioForm?.scrollIntoView({ behavior: 'smooth' });
});

cancelarFuncionarioButton?.addEventListener('click', limparFormularioFuncionario);

presencaForm?.addEventListener('submit', async (event) => {
  event.preventDefault();
  const funcionario = Number(presencaFuncionarioSelect?.value);
  if (!funcionario) {
    presencaStatus.textContent = 'Selecione um funcionário.';
    return;
  }
  registrarPresencaButton.disabled = true;
  presencaStatus.textContent = 'Registrando presença...';
  const obraSelecionada = presencaObraSelect?.value;
  try {
    await post('/presencas/', {
      funcionario,
      obra: obraSelecionada ? Number(obraSelecionada) : null,
    });
    presencaForm.reset();
    await carregarPresencas();
    presencaStatus.textContent = 'Presença registrada com sucesso.';
  } catch (error) {
    presencaStatus.textContent = error.message || 'Não foi possível registrar a presença.';
    registrarPresencaButton.disabled = false;
  }
});

funcionarioForm?.addEventListener('submit', async (event) => {
  event.preventDefault();
  const dados = Object.fromEntries(new FormData(funcionarioForm).entries());
  dados.ativo = document.getElementById('funcionario-ativo').checked;
  funcionarioStatus.textContent = 'Salvando...';
  try {
    let mensagem;
    if (funcionarioEmEdicao) {
      await patch(`/funcionarios/${funcionarioEmEdicao}/`, dados);
      mensagem = 'Funcionário atualizado.';
    } else {
      await post('/funcionarios/', dados);
      mensagem = 'Funcionário cadastrado.';
    }
    limparFormularioFuncionario();
    funcionarioStatus.textContent = mensagem;
    await carregarFuncionarios();
  } catch (error) {
    funcionarioStatus.textContent = error.message || 'Não foi possível salvar o funcionário.';
  }
});

funcionariosLista?.addEventListener('click', async (event) => {
  const botao = event.target.closest('[data-funcionario-acao]');
  if (!botao) return;
  const id = Number(botao.closest('[data-funcionario-id]')?.dataset.funcionarioId);
  if (!id) return;
  try {
    if (botao.dataset.funcionarioAcao === 'editar') {
      preencherFormularioFuncionario(await get(`/funcionarios/${id}/`));
    } else if (botao.dataset.funcionarioAcao === 'excluir' && window.confirm('Excluir este funcionário?')) {
      await remove(`/funcionarios/${id}/`);
      if (funcionarioEmEdicao === id) limparFormularioFuncionario();
      await carregarFuncionarios();
    }
  } catch (error) {
    window.alert(error.message || 'Não foi possível concluir a ação para este funcionário.');
  }
});

obrasLista?.addEventListener('click', async (event) => {
  const botao = event.target.closest('[data-obra-acao]');
  if (!botao) return;
  const id = Number(botao.closest('[data-obra-id]')?.dataset.obraId);
  if (!id) return;
  try {
    const obra = await get(`/obras/${id}/`);
    if (botao.dataset.obraAcao === 'editar') {
      preencherFormularioObra(obra);
    } else if (botao.dataset.obraAcao === 'excluir' && window.confirm(`Excluir ${obra.nome}?`)) {
      await remove(`/obras/${id}/`);
      await carregarObras();
    }
  } catch {
    window.alert('Não foi possível concluir a ação para esta obra.');
  }
});

materiaisLista?.addEventListener('click', async (event) => {
  const botao = event.target.closest('[data-material-acao]');
  if (!botao) return;
  const linha = botao.closest('[data-material-id]');
  const material = materiais.find((item) => item.id === Number(linha?.dataset.materialId));
  if (!material) return;
  if (botao.dataset.materialAcao === 'editar') {
    preencherFormularioMaterial(material);
    return;
  }
  if (botao.dataset.materialAcao === 'excluir' && window.confirm(`Excluir ${material.nome}?`)) {
    try {
      await remove(`/materiais/${material.id}/`);
      await carregarMateriais();
    } catch {
      window.alert('Não foi possível excluir o material.');
    }
  }
});

cancelarEdicaoButton?.addEventListener('click', limparFormulario);

orcamentosLista?.addEventListener('click', async (event) => {
  const botao = event.target.closest('[data-acao]');
  if (!botao) return;
  const item = botao.closest('[data-orcamento-id]');
  const id = item?.dataset.orcamentoId;
  if (!id) return;

  if (botao.dataset.acao === 'editar') {
    try {
      preencherFormulario(await get(`/orcamentos/${id}/`));
    } catch {
      window.alert('Não foi possível carregar o orçamento.');
    }
    return;
  }

  if (botao.dataset.acao === 'excluir' && window.confirm('Excluir este orçamento?')) {
    try {
      await remove(`/orcamentos/${id}/`);
      if (orcamentoEmEdicao === Number(id)) limparFormulario();
      await carregarOrcamentos();
    } catch {
      window.alert('Não foi possível excluir o orçamento.');
    }
  }
});

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

const calculoHandlers = {
  area: (dados) => calcularArea(dados.comprimento, dados.largura),
  concreto: (dados) => calcularConcreto(dados.comprimento, dados.largura, dados.espessura),
  piso: (dados) => calcularPiso(dados.comprimento, dados.largura, dados.perda_percentual),
  custo: (dados) => estimarCusto(dados.area_m2, dados.preco_unitario),
};

const calculoFormatters = {
  area: (resultado) => `Área: ${Number(resultado.area_m2).toFixed(2)} m²`,
  concreto: (resultado) => `Volume: ${Number(resultado.volume_m3).toFixed(2)} m³`,
  piso: (resultado) => `Compra: ${Number(resultado.area_com_perda_m2).toFixed(2)} m² (área: ${Number(resultado.area_m2).toFixed(2)} m²)`,
  custo: (resultado) => `Custo estimado: ${formatarMoeda(resultado.custo_total)}`,
};

document.querySelectorAll('[data-calculo]').forEach((formulario) => {
  formulario.addEventListener('submit', async (event) => {
    event.preventDefault();
    const tipo = formulario.dataset.calculo;
    const resultadoElement = formulario.querySelector('[data-resultado]');
    const dados = Object.fromEntries(new FormData(formulario).entries());
    resultadoElement.textContent = 'Calculando...';
    resultadoElement.classList.remove('text-red-600');
    try {
      const resultado = await calculoHandlers[tipo](dados);
      resultadoElement.textContent = calculoFormatters[tipo](resultado);
    } catch {
      resultadoElement.textContent = 'Não foi possível realizar o cálculo.';
      resultadoElement.classList.add('text-red-600');
    }
  });
});
