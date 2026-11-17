
'use strict';

const CHAVE = 'edutarefas.tarefas.v1';

let tarefas = carregarTarefas();
let filtroAtual = 'todas';
let instalacaoPendente = null;

const elemento = (seletor) => document.querySelector(seletor);

function carregarTarefas() {
  try {
    const dados = JSON.parse(localStorage.getItem(CHAVE) || '[]');
    return Array.isArray(dados)
      ? dados.filter(t => t && typeof t.titulo === 'string' && t.prazo)
      : [];
  } catch (erro) {
    console.error('Erro ao carregar tarefas:', erro);
    return [];
  }
}

function salvarTarefas() {
  try {
    localStorage.setItem(CHAVE, JSON.stringify(tarefas));
  } catch (erro) {
    alert('Não foi possível salvar as tarefas.');
  }
}

function hojeLocal() {
  const hoje = new Date();
  const ano = hoje.getFullYear();
  const mes = String(hoje.getMonth() + 1).padStart(2, '0');
  const dia = String(hoje.getDate()).padStart(2, '0');
  return `${ano}-${mes}-${dia}`;
}

function dataLocal(data) {
  if (!data) return '';
  const [ano, mes, dia] = data.split('-');
  return `${dia}/${mes}/${ano}`;
}

function status(tarefa) {
  if (tarefa.concluida) {
    if (!tarefa.concluidaEm) return 'Concluída';

    const dataConclusao = tarefa.concluidaEm.slice(0, 10);

    return dataConclusao <= tarefa.prazo
      ? 'Entregue no prazo'
      : 'Entregue com atraso';
  }

  return tarefa.prazo < hojeLocal() ? 'Atrasada' : 'Pendente';
}

function concluirTarefa(indice, concluida) {
  tarefas[indice].concluida = concluida;

  if (concluida) {
    tarefas[indice].concluidaEm = new Date().toISOString();
  } else {
    delete tarefas[indice].concluidaEm;
  }

  salvarTarefas();
  renderizar();
}

function renderizar() {
  const lista = elemento('#listaTarefas');
  const termo = elemento('#busca').value.trim().toLocaleLowerCase('pt-BR');

  lista.replaceChildren();

  const visiveis = tarefas
    .map((t, indice) => ({
      ...t,
      indice,
      situacao: status(t)
    }))
    .filter(t => {
      const texto = [
        t.titulo,
        t.disciplina || '',
        t.observacoes || ''
      ].join(' ').toLocaleLowerCase('pt-BR');

      const corresponde = texto.includes(termo);

      const correspondeFiltro =
        filtroAtual === 'todas' ||
        (filtroAtual === 'pendentes' && t.situacao === 'Pendente') ||
        (filtroAtual === 'concluidas' && t.concluida) ||
        (filtroAtual === 'atrasadas' && t.situacao === 'Atrasada');

      return corresponde && correspondeFiltro;
    })
    .sort((a, b) => a.prazo.localeCompare(b.prazo));

  visiveis.forEach(t => {
    const li = document.createElement('li');
    li.className = 'task-item';

    if (t.concluida) li.classList.add('concluida');
    if (t.situacao === 'Atrasada') li.classList.add('atrasada');

    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.checked = Boolean(t.concluida);
    checkbox.setAttribute('aria-label', 'Marcar tarefa como concluída');

    checkbox.addEventListener('change', () => {
      concluirTarefa(t.indice, checkbox.checked);
    });

    const info = document.createElement('div');
    info.className = 'task-info';

    const titulo = document.createElement('strong');
    titulo.textContent = t.titulo;

    const detalhes = document.createElement('small');
    detalhes.textContent =
      `${t.disciplina || 'Geral'} · Prazo: ${dataLocal(t.prazo)}`;

    const situacao = document.createElement('span');
    situacao.className = 'task-status';
    situacao.textContent = t.situacao;

    const prioridade = document.createElement('small');
    prioridade.textContent = `Prioridade: ${t.prioridade || 'Média'}`;

    const acoes = document.createElement('div');
    acoes.className = 'task-actions';

    const botaoConcluir = document.createElement('button');
    botaoConcluir.type = 'button';
    botaoConcluir.textContent = t.concluida
      ? 'Desfazer conclusão'
      : 'Concluir';

    botaoConcluir.addEventListener('click', () => {
      concluirTarefa(t.indice, !t.concluida);
    });

    const botaoExcluir = document.createElement('button');
    botaoExcluir.type = 'button';
    botaoExcluir.textContent = 'Excluir';

    botaoExcluir.addEventListener('click', () => {
      if (confirm(`Deseja excluir "${t.titulo}"?`)) {
        tarefas.splice(t.indice, 1);
        salvarTarefas();
        renderizar();
      }
    });

    acoes.append(botaoConcluir, botaoExcluir);

    info.append(titulo, detalhes, situacao, prioridade);

    if (t.observacoes) {
      const observacao = document.createElement('small');
      observacao.textContent = `Observação: ${t.observacoes}`;
      info.append(observacao);
    }

    info.append(acoes);
    li.append(checkbox, info);
    lista.append(li);
  });

  elemento('#vazio').hidden = visiveis.length > 0;

  elemento('#totalTarefas').textContent = tarefas.length;

  elemento('#pendentes').textContent =
    tarefas.filter(t => status(t) === 'Pendente').length;

  elemento('#concluidas').textContent =
    tarefas.filter(t => t.concluida).length;

  elemento('#atrasadas').textContent =
    tarefas.filter(t => status(t) === 'Atrasada').length;
}

elemento('#formTarefa').addEventListener('submit', evento => {
  evento.preventDefault();

  const titulo = elemento('#titulo').value.trim();
  const disciplina = elemento('#disciplina').value;
  const prioridade = elemento('#prioridade').value;
  const prazo = elemento('#prazo').value;
  const observacoes = elemento('#observacoes').value.trim();
  const mensagem = elemento('#mensagem');

  if (!titulo || !prazo) {
    mensagem.textContent = 'Preencha o título e o prazo.';
    return;
  }

  const data = new Date(`${prazo}T00:00:00`);

  if (Number.isNaN(data.getTime())) {
    mensagem.textContent = 'Informe uma data válida.';
    return;
  }

  tarefas.push({
    titulo,
    disciplina,
    prioridade,
    prazo,
    observacoes,
    concluida: false,
    criadaEm: new Date().toISOString()
  });

  salvarTarefas();
  evento.target.reset();

  mensagem.textContent = 'Tarefa adicionada com sucesso!';

  filtroAtual = 'todas';

  document.querySelectorAll('[data-filtro]').forEach(botao => {
    botao.classList.toggle('active', botao.dataset.filtro === 'todas');
  });

  renderizar();
});

elemento('#busca').addEventListener('input', renderizar);

document.querySelectorAll('[data-filtro]').forEach(botao => {
  botao.addEventListener('click', () => {
    filtroAtual = botao.dataset.filtro;

    document.querySelectorAll('[data-filtro]').forEach(b => {
      b.classList.toggle('active', b === botao);
    });

    renderizar();
  });
});

elemento('#exportar').addEventListener('click', () => {
  const arquivo = new Blob(
    [JSON.stringify(tarefas, null, 2)],
    { type: 'application/json' }
  );

  const link = document.createElement('a');
  const url = URL.createObjectURL(arquivo);

  link.href = url;
  link.download = 'edutarefas-backup.json';
  link.click();

  URL.revokeObjectURL(url);
});

elemento('#importarArquivo').addEventListener('change', evento => {
  const arquivo = evento.target.files[0];
  if (!arquivo) return;

  const leitor = new FileReader();

  leitor.onload = () => {
    try {
      const dados = JSON.parse(leitor.result);

      if (!Array.isArray(dados)) {
        throw new Error('Arquivo inválido');
      }

      const validas = dados.filter(t =>
        t &&
        typeof t.titulo === 'string' &&
        typeof t.prazo === 'string'
      );

      if (!validas.length && dados.length) {
        throw new Error('Nenhuma tarefa válida encontrada');
      }

      tarefas = validas;
      salvarTarefas();
      renderizar();

      alert('Tarefas importadas com sucesso!');
    } catch (erro) {
      alert('Não foi possível importar esse arquivo.');
    }

    evento.target.value = '';
  };

  leitor.readAsText(arquivo);
});

window.addEventListener('beforeinstallprompt', evento => {
  evento.preventDefault();
  instalacaoPendente = evento;
  elemento('#instalar').hidden = false;
});

elemento('#instalar').addEventListener('click', async () => {
  if (!instalacaoPendente) return;

  instalacaoPendente.prompt();
  await instalacaoPendente.userChoice;

  instalacaoPendente = null;
  elemento('#instalar').hidden = true;
});

if (
  'serviceWorker' in navigator &&
  (location.protocol === 'https:' || location.hostname === 'localhost')
) {
  navigator.serviceWorker.register('service-worker.js')
    .catch(erro => console.error('Erro no modo offline:', erro));
}

renderizar();
