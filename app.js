'use strict';
// Lista de dicionários gravada no armazenamento local do navegador.
const CHAVE = 'edutarefas.tarefas.v1';
let tarefas = carregarTarefas();
let filtroAtual = 'todas';
let instalacaoPendente = null;

function carregarTarefas() {
  try {
    const dados = JSON.parse(localStorage.getItem(CHAVE) || '[]');
    return Array.isArray(dados) ? dados.filter(t => t && typeof t.titulo === 'string' && t.prazo) : [];
  } catch (erro) {
    console.error('Não foi possível ler as tarefas salvas.', erro);
    return [];
  }
}
function salvarTarefas() {
  try { localStorage.setItem(CHAVE, JSON.stringify(tarefas)); }
  catch (erro) { alert('Não foi possível salvar. Verifique o espaço disponível no aparelho.'); }
}
function dataLocal(iso) { const [ano, mes, dia] = iso.split('-'); return `${dia}/${mes}/${ano}`; }
function status(tarefa) {
  if (tarefa.concluida) return 'Concluída';
  const hoje = new Date(); hoje.setHours(0,0,0,0);
  const prazo = new Date(`${tarefa.prazo}T00:00:00`);
  return prazo < hoje ? 'Vencida' : 'Pendente';
}
function renderizar() {
  const termo = document.querySelector('#busca').value.trim().toLocaleLowerCase('pt-BR');
  const lista = document.querySelector('#lista'); lista.replaceChildren();
  const visiveis = tarefas.map((t, i) => ({...t, indice:i, situacao:status(t)})).filter(t => {
    const corresponde = t.titulo.toLocaleLowerCase('pt-BR').includes(termo);
    return corresponde && (filtroAtual === 'todas' || (filtroAtual === 'pendentes' && t.situacao === 'Pendente') || (filtroAtual === 'concluidas' && t.situacao === 'Concluída') || (filtroAtual === 'vencidas' && t.situacao === 'Vencida'));
  }).sort((a,b) => a.prazo.localeCompare(b.prazo));
  visiveis.forEach(t => {
    const li = document.createElement('li'); li.className = `tarefa ${t.situacao === 'Vencida' ? 'vencida' : ''} ${t.concluida ? 'concluida' : ''}`;
    const checkbox = document.createElement('input'); checkbox.type='checkbox'; checkbox.className='check'; checkbox.checked=Boolean(t.concluida); checkbox.setAttribute('aria-label', `Marcar ${t.titulo} como concluída`); checkbox.addEventListener('change',()=>{tarefas[t.indice].concluida=checkbox.checked; salvarTarefas(); renderizar();});
    const info = document.createElement('div'); info.className='tarefa-info';
    const titulo = document.createElement('strong'); titulo.textContent=t.titulo;
    const prazo = document.createElement('small'); prazo.textContent=`${t.situacao} · Prazo: ${dataLocal(t.prazo)}`;
    const acoes=document.createElement('div'); acoes.className='acoes';
    const alternar=document.createElement('button'); alternar.textContent=t.concluida?'Desfazer conclusão':'Concluir'; alternar.addEventListener('click',()=>{tarefas[t.indice].concluida=!tarefas[t.indice].concluida; salvarTarefas(); renderizar();});
    const apagar=document.createElement('button'); apagar.textContent='Excluir'; apagar.className='apagar'; apagar.addEventListener('click',()=>{if(confirm(`Excluir “${t.titulo}”?`)){tarefas.splice(t.indice,1);salvarTarefas();renderizar();}});
    acoes.append(alternar,apagar); info.append(titulo,prazo,acoes); li.append(checkbox,info); lista.append(li);
  });
  document.querySelector('#vazio').hidden=visiveis.length>0;
  document.querySelector('#total').textContent=tarefas.length;
  document.querySelector('#feitas').textContent=tarefas.filter(t=>t.concluida).length;
  document.querySelector('#abertas').textContent=tarefas.filter(t=>!t.concluida).length;
}
document.querySelector('#form-tarefa').addEventListener('submit', evento=>{
  evento.preventDefault(); const titulo=document.querySelector('#titulo').value.trim(); const prazo=document.querySelector('#prazo').value;
  if(!titulo || !prazo){document.querySelector('#aviso').textContent='Preencha o título e o prazo.';return;}
  // Validar a data real, além do formato fornecido pelo navegador.
  const data=new Date(`${prazo}T00:00:00`);
  if(Number.isNaN(data.getTime()) || data.toISOString().slice(0,10)!==prazo){document.querySelector('#aviso').textContent='Informe uma data válida.';return;}
  tarefas.push({titulo,prazo,concluida:false,criadaEm:new Date().toISOString()}); salvarTarefas(); evento.target.reset(); document.querySelector('#aviso').textContent='Tarefa adicionada.'; filtroAtual='todas'; document.querySelectorAll('[data-filtro]').forEach(b=>b.classList.toggle('ativo',b.dataset.filtro==='todas')); renderizar();
});
document.querySelector('#busca').addEventListener('input',renderizar);
document.querySelectorAll('[data-filtro]').forEach(botao=>botao.addEventListener('click',()=>{filtroAtual=botao.dataset.filtro;document.querySelectorAll('[data-filtro]').forEach(b=>b.classList.toggle('ativo',b===botao));renderizar();}));
document.querySelector('#exportar').addEventListener('click',()=>{const blob=new Blob([JSON.stringify(tarefas,null,2)],{type:'application/json'});const link=document.createElement('a');link.href=URL.createObjectURL(blob);link.download='edutarefas-backup.json';link.click();URL.revokeObjectURL(link.href);});
window.addEventListener('beforeinstallprompt',e=>{e.preventDefault();instalacaoPendente=e;document.querySelector('#instalar').hidden=false;});
document.querySelector('#instalar').addEventListener('click',async()=>{if(!instalacaoPendente)return;instalacaoPendente.prompt();await instalacaoPendente.userChoice;instalacaoPendente=null;document.querySelector('#instalar').hidden=true;});
if('serviceWorker' in navigator && (location.protocol==='https:' || location.hostname==='localhost')) navigator.serviceWorker.register('service-worker.js').catch(err=>console.error('Falha ao preparar modo offline:',err));
renderizar();
