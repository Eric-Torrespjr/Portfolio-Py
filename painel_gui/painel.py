"""
Automação 3 — Painel com interface gráfica (tkinter)
Demonstra: UX simples para operação, chamadas HTTP assíncronas em thread (sem travar UI),
orquestração entre script de integração e API local.
"""
from __future__ import annotations

import subprocess
import sys
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext
from pathlib import Path

import httpx

BASE_DIR = Path(__file__).resolve().parent.parent
INTEGRADOR = BASE_DIR / "integrador_dados_api" / "sincronizar_usuarios.py"
API_HEALTH = "http://127.0.0.1:8000/health"
API_TAREFAS = "http://127.0.0.1:8000/tarefas"


class PainelAutomacao(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Painel — Automação & APIs (demo portfólio)")
        self.geometry("720x520")
        self.minsize(560, 400)

        frm = tk.Frame(self, padx=12, pady=12)
        frm.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            frm,
            text="Orquestra integrações e testa a API REST local",
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor=tk.W)

        tk.Label(
            frm,
            text=(
                "1) Suba o serviço: python -m uvicorn servico_rest.app:app --reload\n"
                "2) Use os botões abaixo (logs aparecem na área de texto)."
            ),
            justify=tk.LEFT,
            font=("Segoe UI", 9),
        ).pack(anchor=tk.W, pady=(4, 12))

        bf = tk.Frame(frm)
        bf.pack(fill=tk.X, pady=(0, 8))

        tk.Button(bf, text="Rodar sincronização (API pública → CSV)", command=self._sync_click).pack(
            side=tk.LEFT, padx=(0, 8)
        )
        tk.Button(bf, text="GET /health (API local)", command=self._health_click).pack(side=tk.LEFT, padx=(0, 8))
        tk.Button(bf, text="Listar tarefas (GET /tarefas)", command=self._listar_click).pack(side=tk.LEFT)

        self.log = scrolledtext.ScrolledText(frm, height=22, font=("Consolas", 10), state=tk.DISABLED)
        self.log.pack(fill=tk.BOTH, expand=True, pady=(8, 0))

        self._log_line("Painel iniciado. Pronto.\n")

    def _log_line(self, msg: str) -> None:
        self.log.configure(state=tk.NORMAL)
        self.log.insert(tk.END, msg)
        self.log.see(tk.END)
        self.log.configure(state=tk.DISABLED)

    def _run_in_thread(self, fn) -> None:
        def wrap():
            try:
                fn()
            except Exception as e:
                self.after(0, lambda: self._log_line(f"Erro: {e}\n"))

        threading.Thread(target=wrap, daemon=True).start()

    def _sync_click(self) -> None:
        def job():
            self.after(0, lambda: self._log_line("Executando sincronizador...\n"))
            proc = subprocess.run(
                [sys.executable, str(INTEGRADOR)],
                cwd=str(BASE_DIR),
                capture_output=True,
                text=True,
                timeout=120,
            )
            out = (proc.stdout or "") + (proc.stderr or "")
            self.after(0, lambda o=out, c=proc.returncode: self._log_line(o + (f"\n[Código saída: {c}]\n" if c else "\n[OK]\n")))

        self._run_in_thread(job)

    def _health_click(self) -> None:
        def job():
            self.after(0, lambda: self._log_line("GET health...\n"))
            try:
                with httpx.Client(timeout=10.0) as client:
                    r = client.get(API_HEALTH)
                    body = r.json() if r.headers.get("content-type", "").startswith("application/json") else r.text
                self.after(
                    0,
                    lambda: self._log_line(f"Status {r.status_code}: {body}\n\n"),
                )
            except httpx.RequestError as e:
                self.after(
                    0,
                    lambda: self._log_line(
                        f"Não foi possível conectar em {API_HEALTH}\n"
                        f"Inicie o uvicorn em outro terminal. Detalhe: {e}\n\n"
                    ),
                )

        self._run_in_thread(job)

    def _listar_click(self) -> None:
        def job():
            self.after(0, lambda: self._log_line("GET /tarefas...\n"))
            try:
                with httpx.Client(timeout=10.0) as client:
                    r = client.get(API_TAREFAS)
                    body = r.json() if r.headers.get("content-type", "").startswith("application/json") else r.text
                texto = str(body)
                if len(texto) > 4000:
                    texto = texto[:4000] + "\n... (truncado)"
                self.after(0, lambda: self._log_line(f"Status {r.status_code}:\n{texto}\n\n"))
            except httpx.RequestError as e:
                self.after(
                    0,
                    lambda: messagebox.showwarning(
                        "API local",
                        f"Serviço não disponível.\n{e}",
                    ),
                )

        self._run_in_thread(job)


def main() -> None:
    app = PainelAutomacao()
    app.mainloop()


if __name__ == "__main__":
    main()
