"""
Demo única: chatbot (comandos em texto) + processo de pedidos + dashboard.
Execute: streamlit run chatbot_processo_dashboard/app.py
"""
from __future__ import annotations

import pandas as pd
import streamlit as st

from processo import (
    avancar_um_pedido,
    consulta_api_demo,
    listar_pedidos,
    registrar_pedido,
)

st.set_page_config(
    page_title="Chatbot & processo & dashboard",
    page_icon="⚡",
    layout="wide",
)


def responder(mensagem: str) -> str:
    texto = mensagem.strip()
    if not texto:
        return "Escreva um comando ou diga **ajuda**."
    t = texto.lower()

    if t in ("ajuda", "help", "?"):
        return (
            "**Comandos simples:**\n\n"
            "| Você digita | O que acontece |\n"
            "|-------------|----------------|\n"
            "| `pedido: nome, quantidade` | Registra pedido (ex: `pedido: Café, 5`) |\n"
            "| `processar` | Avança um pedido no fluxo interno |\n"
            "| `api` | Chama API externa de demo e mostra o retorno |\n"
            "| `status` | Resumo rápido dos pedidos |\n"
        )

    if t.startswith("pedido:"):
        corpo = texto.split(":", 1)[1].strip()
        if "," not in corpo:
            return "Use: `pedido: item, quantidade` — exemplo: `pedido: Caderno, 3`"
        item, qtd_raw = corpo.rsplit(",", 1)
        try:
            qtd = int(qtd_raw.strip())
        except ValueError:
            return "A quantidade precisa ser um número inteiro."
        if qtd < 1:
            return "Quantidade deve ser pelo menos 1."
        p = registrar_pedido(item, qtd)
        return (
            f"Registrado pedido **#{p['id']}**: {p['item']} × {p['quantidade']} "
            f"(estimado R$ {p['valor_estimado']:.2f}). Status: **{p['status']}**."
        )

    if "processar" in t:
        msg, _ = avancar_um_pedido()
        return msg or "Não há pedido para avançar no momento."

    if any(k in t for k in ("api", "externo", "integrar")):
        try:
            d = consulta_api_demo()
        except Exception as e:
            return f"Falha na API de demo (verifique a rede): `{e}`"
        return (
            "**Integração OK (demo):** título da tarefa externa: "
            f"_{d.get('title', '')}_ — concluída: `{d.get('completed')}`"
        )

    if "status" in t or "resumo" in t:
        rows = listar_pedidos()
        if not rows:
            return "Ainda não há pedidos. Registre com `pedido: item, qtd`."
        por_status = {}
        for r in rows:
            por_status[r["status"]] = por_status.get(r["status"], 0) + 1
        partes = [f"**{k}:** {v}" for k, v in sorted(por_status.items())]
        total = sum(r["valor_estimado"] for r in rows)
        return f"Total **{len(rows)}** pedidos. " + " · ".join(partes) + f" · Valor estimado somado: **R$ {total:.2f}**"

    return "Não reconheci. Tente **ajuda**."


def painel_dashboard() -> None:
    rows = listar_pedidos()
    st.subheader("Dashboard do processo")
    if not rows:
        st.info("Sem dados ainda — use o chat para registrar um `pedido: ...`.")
        return

    df = pd.DataFrame(rows)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Pedidos", len(df))
    c2.metric("Pendentes", int((df["status"] == "pendente").sum()))
    c3.metric("Em separação", int((df["status"] == "em_separacao").sum()))
    c4.metric("Concluídos", int((df["status"] == "concluido").sum()))

    st.caption("Distribuição por status")
    contagem = df["status"].value_counts()
    st.bar_chart(contagem)

    st.subheader("Últimos registros")
    exibir = df.sort_values("id", ascending=False).head(12)
    st.dataframe(exibir, use_container_width=True, hide_index=True)


def main() -> None:
    st.title("Chatbot + integração de processos + dashboard")
    st.caption("Fluxo didático e simples — um único app Streamlit.")

    tab_chat, tab_dash = st.tabs(["💬 Chat", "📊 Dashboard"])

    with tab_chat:
        if "msgs" not in st.session_state:
            st.session_state.msgs = [
                (
                    "assistant",
                    "Olá! Sou um assistente **por comandos**. Digite **ajuda** para ver o que posso fazer.",
                )
            ]
        for role, content in st.session_state.msgs:
            with st.chat_message(role):
                st.markdown(content)

        if prompt := st.chat_input("Ex.: ajuda | pedido: Tinta, 2 | processar | api | status"):
            st.session_state.msgs.append(("user", prompt))
            st.session_state.msgs.append(("assistant", responder(prompt)))
            st.rerun()

    with tab_dash:
        painel_dashboard()


if __name__ == "__main__":
    main()
