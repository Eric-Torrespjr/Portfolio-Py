"""
Integração de processos (camada simples): pedidos em arquivo JSON
+ uma chamada HTTP de exemplo para simular enriquecimento via API.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import httpx

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "pedidos_demo.json"


def _carregar() -> list[dict]:
    if not DATA_FILE.exists():
        return []
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def _salvar(rows: list[dict]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")


def listar_pedidos() -> list[dict]:
    return _carregar()


def registrar_pedido(item: str, quantidade: int, cliente: str = "Chat") -> dict:
    rows = _carregar()
    novo_id = max((r["id"] for r in rows), default=0) + 1
    registro = {
        "id": novo_id,
        "cliente": cliente.strip() or "Chat",
        "item": item.strip(),
        "quantidade": int(quantidade),
        "status": "pendente",
        "valor_estimado": round(float(quantidade) * 49.9, 2),
        "criado_em": datetime.now(timezone.utc).isoformat(),
    }
    rows.append(registro)
    _salvar(rows)
    return registro


def avancar_um_pedido() -> tuple[str | None, list[dict]]:
    """Move um pedido no fluxo: pendente → em_separacao → concluido."""
    rows = _carregar()
    agora = datetime.now(timezone.utc).isoformat()
    for alvo in ("pendente", "em_separacao"):
        for r in rows:
            if r["status"] != alvo:
                continue
            if alvo == "pendente":
                r["status"] = "em_separacao"
                msg = f"Pedido #{r['id']} passou para **em separação**."
            else:
                r["status"] = "concluido"
                msg = f"Pedido #{r['id']} **concluído**."
            r["atualizado_em"] = agora
            _salvar(rows)
            return msg, rows
    _salvar(rows)
    return None, rows


def consulta_api_demo() -> dict:
    """Consumo de API REST pública (sem chave) — ilustra ponto de integração."""
    url = "https://jsonplaceholder.typicode.com/todos/1"
    with httpx.Client(timeout=15.0) as client:
        resp = client.get(url)
        resp.raise_for_status()
        return resp.json()
