# Chatbot + processo + dashboard (simples)

Um único aplicativo **Streamlit** que junta três ideias com pouco código:

| Parte | O que é |
|-------|---------|
| **Chatbot** | Você digita comandos em português (`ajuda`, `pedido: ...`, `processar`, `api`, `status`). Não usa LLM pago — é regra + texto, fácil de entender e estender. |
| **Integração de processos** | Pedidos são gravados em `data/pedidos_demo.json` e avançam em fluxo: `pendente` → `em_separacao` → `concluido`. O comando `api` chama uma REST pública (JSONPlaceholder) para similar **integração externa**. |
| **Dashboard** | Aba com métricas (`st.metric`), gráfico de barras por status e tabela dos últimos pedidos. |

## Rodar

Na pasta raiz do repositório `automacoes`:

```powershell
.\.venv\Scripts\pip install -r requirements.txt
.\.venv\Scripts\streamlit run chatbot_processo_dashboard\app.py
```

Abre no navegador (geralmente `http://localhost:8501`).

## Por que é mais simples que os outros exemplos?

- Tudo em **um** comando para subir (`streamlit run`).
- Lógica de negócio separada em `processo.py`; a interface só chama funções.
- Chatbot **explícito** (sem caixa-preta de modelo).

## Extensões possíveis (currículo / entrevista)

- Plugue um **Blip** ou **Dialogflow** no lugar das regras do `responder()`.
- Troque o JSON por **API interna** ou banco.
- Publique o dashboard com **Streamlit Community Cloud**.
