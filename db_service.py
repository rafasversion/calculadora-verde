import json
from pathlib import Path

ARQUIVO = Path("datacenters.json")


def _carregar():
    if ARQUIVO.exists():
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"datacenters": []}


def _salvar(dados):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)


def listar_datacenters():
    dados = _carregar()
    return dados["datacenters"]


def buscar_datacenter(datacenter_id):
    datacenters = listar_datacenters()
    for d in datacenters:
        if d["id"] == datacenter_id:
            return d
    return None


def adicionar_datacenter(nome):
    dados = _carregar()

    datacenters = dados["datacenters"]
    novo_id = 1
    if datacenters:
        novo_id = max(d["id"] for d in datacenters) + 1

    novo_datacenter = {"id": novo_id, "nome": nome}
    datacenters.append(novo_datacenter)

    _salvar(dados)
    return novo_datacenter


def remover_datacenter(datacenter_id):
    dados = _carregar()
    datacenters = dados["datacenters"]

    dados["datacenters"] = [d for d in datacenters if d["id"] != datacenter_id]

    _salvar(dados)
