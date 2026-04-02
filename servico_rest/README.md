# Automação — API REST com FastAPI (CRUD de tarefas)

## O que faz

Este módulo expõe um **serviço REST** construído com **FastAPI**, demonstrando **construção** (não só consumo) de APIs:

- **`GET /health`** — verificação de disponibilidade para monitoramento ou orquestradores.
- **`GET /tarefas`** — lista todas as tarefas.
- **`GET /tarefas/{id}`** — obtém uma tarefa.
- **`POST /tarefas`** — cria tarefa (corpo JSON com título, descrição opcional, prioridade `baixa` | `media` | `alta`).
- **`PATCH /tarefas/{id}`** — atualiza campos parciais e marca conclusão.
- **`DELETE /tarefas/{id}`** — remove a tarefa.

Os dados ficam em **memória** (adequado para demo e testes). Em projeto real, a mesma interface evolui para banco de dados ou fila.

A documentação interativa **OpenAPI (Swagger)** fica em **`/docs`** quando o servidor está no ar — boa prática de **documentação viva** para times e integradores.

## Como executar

Na raiz do projeto:

```bash
.\.venv\Scripts\pip install -r requirements.txt
.\.venv\Scripts\python -m uvicorn servico_rest.app:app --reload --host 127.0.0.1 --port 8000
```

Abra no navegador: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Exemplo rápido (PowerShell)

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/tarefas -ContentType "application/json" -Body '{"titulo":"Demo","prioridade":"alta"}'
```

## Stack

FastAPI, Pydantic, Uvicorn.
