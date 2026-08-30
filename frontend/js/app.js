import { calcularArea } from './api.js';

const formArea = document.getElementById('form-area');
const resultadoArea = document.getElementById('resultado-area');
const offlineStatus = document.getElementById('offline-status');

function updateOnlineStatus() {
  offlineStatus.textContent = navigator.onLine ? 'Conectado' : 'Modo offline — dados em cache';
}

window.addEventListener('online', updateOnlineStatus);
window.addEventListener('offline', updateOnlineStatus);
updateOnlineStatus();

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
