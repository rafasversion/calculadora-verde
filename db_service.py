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
    """Busca um datacenter pelo seu ID numérico."""
    datacenters = listar_datacenters()
    for d in datacenters:
        if d.get("id") == datacenter_id:
            return d
    return None

def buscar_por_codigo(codigo):
    """Busca um datacenter pelo seu código (ex: DC-SP01)."""
    datacenters = listar_datacenters()
    for d in datacenters:
        if d.get("codigo") == codigo:
            return d
    return None


def adicionar_datacenter(datacenter_obj):

    dados = _carregar()
    datacenters = dados["datacenters"]
    novo_id = 1
    if datacenters:
        novo_id = max(d.get("id", 0) for d in datacenters) + 1

    datacenter_obj["id"] = novo_id
    datacenters.append(datacenter_obj)
    _salvar(dados)
    return datacenter_obj



def deletar_datacenter(datacenter_id):
    dados = _carregar()
    datacenters = dados["datacenters"]

    dados["datacenters"] = [
        dc for dc in datacenters if dc.get("id") != datacenter_id
    ]

    _salvar(dados)
    return True

