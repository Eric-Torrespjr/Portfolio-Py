"""
Automação 2 — API REST com FastAPI (construção de APIs)
Demonstra: modelos Pydantic, CRUD em memória, documentação OpenAPI automática (/docs).
Ideal para integrações internas ou camada intermediária em transformação digital.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="API de Tarefas — Demo Automação",
    description="Exemplo de API REST para rotinas de back-office e integração.",
    version="1.0.0",
)

# Armazenamento em memória (demo). Em produção: banco ou fila.
_tarefas: dict[int, dict] = {}
_proximo_id = 1


def agora_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class TarefaCreate(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=200)
    descricao: Optional[str] = Field(None, max_length=2000)
    prioridade: str = Field("media", pattern="^(baixa|media|alta)$")


class TarefaUpdate(BaseModel):
    titulo: Optional[str] = Field(None, min_length=1, max_length=200)
    descricao: Optional[str] = None
    prioridade: Optional[str] = Field(None, pattern="^(baixa|media|alta)$")
    concluida: Optional[bool] = None


class Tarefa(BaseModel):
    id: int
    titulo: str
    descricao: Optional[str]
    prioridade: str
    concluida: bool
    criada_em: str
    atualizada_em: str


@app.get("/health")
def health():
    return {"status": "ok", "servico": "tarefas-demo", "timestamp": agora_iso()}


@app.get("/tarefas", response_model=list[Tarefa])
def listar_tarefas():
    return [Tarefa(**t) for t in _tarefas.values()]


@app.get("/tarefas/{tarefa_id}", response_model=Tarefa)
def obter_tarefa(tarefa_id: int):
    if tarefa_id not in _tarefas:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return Tarefa(**_tarefas[tarefa_id])


@app.post("/tarefas", response_model=Tarefa, status_code=201)
def criar_tarefa(body: TarefaCreate):
    global _proximo_id
    now = agora_iso()
    tid = _proximo_id
    _proximo_id += 1
    reg = {
        "id": tid,
        "titulo": body.titulo,
        "descricao": body.descricao,
        "prioridade": body.prioridade,
        "concluida": False,
        "criada_em": now,
        "atualizada_em": now,
    }
    _tarefas[tid] = reg
    return Tarefa(**reg)


@app.patch("/tarefas/{tarefa_id}", response_model=Tarefa)
def atualizar_tarefa(tarefa_id: int, body: TarefaUpdate):
    if tarefa_id not in _tarefas:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    reg = _tarefas[tarefa_id].copy()
    if body.titulo is not None:
        reg["titulo"] = body.titulo
    if body.descricao is not None:
        reg["descricao"] = body.descricao
    if body.prioridade is not None:
        reg["prioridade"] = body.prioridade
    if body.concluida is not None:
        reg["concluida"] = body.concluida
    reg["atualizada_em"] = agora_iso()
    _tarefas[tarefa_id] = reg
    return Tarefa(**reg)


@app.delete("/tarefas/{tarefa_id}", status_code=204)
def remover_tarefa(tarefa_id: int):
    if tarefa_id not in _tarefas:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    del _tarefas[tarefa_id]
    return None
