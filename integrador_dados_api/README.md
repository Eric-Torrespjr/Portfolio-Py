# Automação — Integração de dados via API REST

## O que faz

Este script automatiza um fluxo típico de **integração de sistemas**:

1. **Consome** a API REST pública [JSONPlaceholder](https://jsonplaceholder.typicode.com/) (`GET /users`), sem necessidade de chave ou cadastro.
2. **Normaliza** os dados: achata campos aninhados (endereço e empresa) em colunas simples, prontas para relatório ou carga em outro sistema.
3. **Persiste** o resultado em arquivo **CSV** com nome horário (`data/usuarios_YYYYMMDD_HHMMSS.csv`), permitindo histórico de execuções.
4. **Registra** cada etapa em **log** (`data/sincronizacao.log`), em UTC, com nível INFO e erros capturados.

Em resumo: é uma rotina de **ETL leve** (extract → transform → load) acionada por linha de comando, alinhada a cenários de **ganho de eficiência** e **rastreabilidade** em automação corporativa.

## Como executar

Na raiz do projeto (`automacoes`):

```bash
python -m venv .venv
# Windows:
.\.venv\Scripts\pip install -r requirements.txt
.\.venv\Scripts\python integrador_dados_api\sincronizar_usuarios.py
```

## Requisitos

Dependências na raiz: `httpx` (e demais pacotes listados em `requirements.txt`).

## Saídas

| Local | Conteúdo |
|-------|----------|
| `data/usuarios_*.csv` | Usuários exportados após cada execução bem-sucedida |
| `data/sincronizacao.log` | Linhas de log append |
