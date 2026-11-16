# Como executar e explicar o projeto

## Versão desktop

Requer Python 3 instalado. No terminal, dentro da pasta `edutarefas-pwa`:

```bash
python desktop.py
```

A biblioteca Tkinter normalmente acompanha a instalação padrão do Python.

## Versão web Flask (computador)

```bash
python -m pip install -r requirements.txt
python app.py
```

Abra `http://127.0.0.1:5000` no navegador. O arquivo `tarefas.json` será criado automaticamente na mesma pasta.

## Abrir Flask no celular pela rede local

O celular e o computador precisam estar na mesma rede Wi-Fi. Inicie o Flask pelo comando acima e descubra o endereço IP local do computador (por exemplo, `192.168.1.20`). No celular, abra `http://192.168.1.20:5000`. O firewall do computador pode precisar permitir conexões na porta 5000. Para acesso fora da rede local, publique o Flask em um serviço que hospede aplicações Python.

## Versão PWA publicada no GitHub Pages

Consulte `README.md`; use os arquivos da pasta `docs`. Essa variante pode ser instalada na tela inicial e funciona offline após carregar uma vez. Ela guarda dados no armazenamento do próprio navegador, separado do `tarefas.json` do Flask/Tkinter.

## Estrutura de dados e funções

O sistema usa uma lista de dicionários. Cada dicionário representa uma tarefa com título, prazo, situação e horário de criação. `dados.py` centraliza carregamento, gravação JSON, inclusão, busca, cálculo de status, alternância e remoção; as interfaces desktop e Flask chamam as mesmas funções.

O projeto aplica entrada (formulários), processamento (validação, condicionais, filtros e estatísticas) e saída (lista, contadores e mensagens); tipos `str`, `bool` e listas/dicionários; funções com `def`; decisões `if/else`; laços `for`; tratamento de erros `try/except`; e persistência em arquivo JSON.

A PWA é uma versão adicional para o celular. O GitHub Pages não executa Python ou Flask: serve somente os arquivos estáticos da pasta `mobile`. Para compartilhar as mesmas tarefas entre celular e computador, seria necessário hospedar o Flask em um servidor Python e fazer a PWA se conectar a essa API.
