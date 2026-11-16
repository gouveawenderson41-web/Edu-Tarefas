# EduTarefas — projeto Python com versão para celular

O projeto reúne as interfaces exigidas para a atividade (Tkinter e Flask), uma camada comum em Python que grava tarefas em JSON e uma versão móvel instalável (PWA) publicável no GitHub Pages.

## Instalar no celular pelo GitHub Pages

1. Crie um repositório no GitHub e envie os arquivos deste projeto.
2. Abra **Settings → Pages**.
3. Em **Build and deployment**, escolha **Deploy from a branch**, selecione a branch `main` e a pasta `/docs`.
4. Abra no celular o endereço HTTPS que o GitHub Pages mostrar.
5. Android/Chrome: menu ⋮ → **Instalar app** ou **Adicionar à tela inicial**. iPhone/Safari: **Compartilhar → Adicionar à Tela de Início**.

Após o primeiro acesso com internet, a interface da PWA fica disponível offline. As tarefas desta versão ficam salvas no próprio navegador/aparelho. Use **Exportar dados** para baixar uma cópia JSON. A PWA não sincroniza com o `tarefas.json` usado pelas versões Flask e Tkinter.

## Executar as versões Python

Veja [COMO_USAR.md](COMO_USAR.md) para instruções da versão desktop e da versão Flask, inclusive como acessar o Flask pelo celular na mesma rede Wi-Fi.

## Conteúdos da apostila aplicados

- dados de entrada, processamento e saída;
- variáveis e tipos primitivos;
- condicionais e laços;
- lista de dicionários;
- funções e módulos;
- validação e tratamento de erros;
- gravação e leitura de dados em JSON.

## Organização

- `dados.py`: funções de persistência, validação, busca, filtros e estatísticas, compartilhadas por Tkinter e Flask.
- `desktop.py`: interface desktop Tkinter.
- `app.py`: rotas da aplicação Flask.
- `templates/index.html`: interface web responsiva.
- `static/estilo.css`: estilos da versão Flask.
- `docs/`: PWA pronta para publicação no GitHub Pages.
- `mobile/`: cópia de trabalho dos arquivos da PWA.
# EduTarefas
# EduTarefas
