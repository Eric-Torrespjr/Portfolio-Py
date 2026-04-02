# Automação — Painel gráfico (tkinter)

## O que faz

Interface desktop simples que **orquestra** os outros componentes do repositório, útil para simular um **operador** ou área de negócio disparando rotinas sem usar o terminal:

1. **Rodar sincronização** — executa o script `integrador_dados_api/sincronizar_usuarios.py` em subprocesso e mostra a saída no painel de texto.
2. **GET /health** — chama a API local em `http://127.0.0.1:8000/health` para validar se o serviço FastAPI está no ar.
3. **Listar tarefas** — chama `GET http://127.0.0.1:8000/tarefas` e exibe o JSON retornado (truncado se for muito grande).

As requisições HTTP e o subprocesso rodam em **threads** em segundo plano para **não travar** a janela (evita congelar a UI durante rede ou I/O).

Para usar os botões da API local, é preciso ter o Uvicorn rodando (veja `servico_rest/README.md`).

## Como executar

Terminal 1 — API (opcional, para testar health e tarefas):

```bash
cd automacoes
.\.venv\Scripts\python -m uvicorn servico_rest.app:app --reload --host 127.0.0.1 --port 8000
```

Terminal 2 — painel:

```bash
cd automacoes
.\.venv\Scripts\python painel_gui\painel.py
```

## Requisitos

Python com `tkinter` (incluso na maioria das instalações oficiais no Windows) e `httpx` (instalado via `requirements.txt` na raiz).
