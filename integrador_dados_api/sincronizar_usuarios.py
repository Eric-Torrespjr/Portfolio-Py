"""
Automação 1 — Integração de dados via API REST
Demonstra: consumo de API, normalização, persistência (CSV) e logging estruturado.
Fonte pública: JSONPlaceholder (sem chave).
"""
from __future__ import annotations

import csv
import logging
import time
from datetime import datetime, timezone
from pathlib import Path

import httpx

API_URL = "https://jsonplaceholder.typicode.com/users"
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
LOG_FILE = DATA_DIR / "sincronizacao.log"


def configurar_logging() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%SZ",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
    logging.Formatter.converter = time.gmtime


def buscar_usuarios() -> list[dict]:
    logging.info("Iniciando GET %s", API_URL)
    with httpx.Client(timeout=30.0) as client:
        response = client.get(API_URL)
        response.raise_for_status()
        dados = response.json()
    logging.info("Recebidos %s registros", len(dados))
    return dados


def normalizar_linhas(usuarios: list[dict]) -> list[dict]:
    """Achata endereço e empresa para colunas tabulares (ETL leve)."""
    linhas: list[dict] = []
    for u in usuarios:
        end = u.get("address") or {}
        comp = u.get("company") or {}
        linhas.append(
            {
                "id": u.get("id"),
                "nome": u.get("name"),
                "usuario": u.get("username"),
                "email": u.get("email"),
                "telefone": u.get("phone"),
                "site": u.get("website"),
                "cidade": end.get("city"),
                "rua": end.get("street"),
                "cep": end.get("zipcode"),
                "empresa": comp.get("name"),
                "slogan": (comp.get("catchPhrase") or "")[:80],
            }
        )
    return linhas


def exportar_csv(linhas: list[dict], destino: Path) -> None:
    if not linhas:
        logging.warning("Nada para exportar.")
        return
    campos = list(linhas[0].keys())
    with destino.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        w.writerows(linhas)
    logging.info("CSV gravado em %s (%s linhas)", destino, len(linhas))


def main() -> None:
    configurar_logging()
    try:
        raw = buscar_usuarios()
        linhas = normalizar_linhas(raw)
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        arquivo = DATA_DIR / f"usuarios_{ts}.csv"
        exportar_csv(linhas, arquivo)
        logging.info("Sincronização concluída com sucesso.")
    except httpx.HTTPError as e:
        logging.exception("Falha HTTP: %s", e)
        raise SystemExit(1) from e


if __name__ == "__main__":
    main()
