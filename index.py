from flask import Flask, request, render_template, redirect, url_for
from calculador import (
    calcular_pue, calcular_cue, calcular_dcie, calcular_wue,
    calcular_angulo_pue, calcular_angulo_cue, calcular_angulo_dcie, calcular_angulo_wue
)
import db_service as db
import datetime

app = Flask(__name__)


@app.route("/")
def homepage():
    datacenters = db.listar_datacenters()

    media_pue = 1.0 
    media_cue = 0.0
    media_dcie = 0.0
    media_wue = 0.0

    if datacenters:
        def somar_indicador(indicador_key):
            soma = 0.0
            contagem = 0
            for dc in datacenters:
                valor_str = dc.get("indicadores", {}).get(indicador_key)
                if valor_str:
                    try:
                        soma += float(valor_str)
                        contagem += 1
                    except ValueError:
                        pass
            return soma, contagem

        
        soma_pue, total_pue = somar_indicador("pue")
        soma_cue, total_cue = somar_indicador("cue")
        soma_dcie, total_dcie = somar_indicador("dcie")
        soma_wue, total_wue = somar_indicador("wue")

      
        media_pue = soma_pue / total_pue if total_pue > 0 else 1.0
        media_cue = soma_cue / total_cue if total_cue > 0 else 0.0
        media_dcie = soma_dcie / total_dcie if total_dcie > 0 else 0.0
        media_wue = soma_wue / total_wue if total_wue > 0 else 0.0
    
    angulo_pue = calcular_angulo_pue(media_pue)
    angulo_cue = calcular_angulo_cue(media_cue)
    angulo_dcie = calcular_angulo_dcie(media_dcie)
    angulo_wue = calcular_angulo_wue(media_wue) 

    return render_template(
        "homepage.html",
        datacenters=datacenters,
        angulo_pue=angulo_pue,
        angulo_cue=angulo_cue,
        angulo_dcie=angulo_dcie,
        angulo_wue=angulo_wue,
      
        media_pue=f"{media_pue:.2f}",
        media_cue=f"{media_cue:.2f}",
        media_dcie=f"{media_dcie:.2f}",
        media_wue=f"{media_wue:.2f}"
    )

@app.route("/metricas")
def metricas():
    return render_template("metricas.html")

@app.route("/datacenter/<codigo>")
def pagina_datacenter(codigo):
    dc = db.buscar_por_codigo(codigo)

    if not dc:
        return f"Datacenter '{codigo}' não encontrado.", 404

    def get_indicador_float(key, default_value=0.0):
        try:
            return float(dc["indicadores"].get(key, default_value))
        except (ValueError, TypeError):
            return default_value

    pue = get_indicador_float("pue", 1.0) 
    cue = get_indicador_float("cue", 0.0)
    dcie = get_indicador_float("dcie", 0.0)
    wue = get_indicador_float("wue", 0.0)

    angulo_pue = calcular_angulo_pue(pue)
    angulo_cue = calcular_angulo_cue(cue)
    angulo_dcie = calcular_angulo_dcie(dcie)
    angulo_wue = calcular_angulo_wue(wue) 

    return render_template(
        "datacenter.html",
        datacenter=dc,
        angulo_pue=angulo_pue,
        angulo_cue=angulo_cue,
        angulo_dcie=angulo_dcie,
        angulo_wue=angulo_wue
    )


@app.route("/api/datacenters", methods=["POST"])
def api_adicionar_datacenter():
    form = request.form

    codigo = form.get("codigo", "").strip()
    nome = form.get("nome", "").strip()
    endereco = form.get("endereco", "").strip()
    latitude = form.get("latitude", "").strip() or None
    longitude = form.get("longitude", "").strip() or None

    proprietario = form.get("proprietario", "").strip()
    tipo = form.get("tipo_operacao", "").strip()
    data_inicio = form.get("data_inicio", "").strip()
    status = form.get("status", "").strip()
    sla = form.get("sla_disponibilidade", "").strip()

    capacidade_kw = form.get("capacidade_kw", "").strip()
    clima_tipo = form.get("clima_tipo", "").strip()
    carriers_raw = form.get("carriers", "").strip()
    uplink_total_Gbps = form.get("uplink_total_Gbps", "").strip()

    if not nome or not codigo or not proprietario or not capacidade_kw:
        return "Campos obrigatórios faltando", 400

    try:
        capacidade_kw = float(capacidade_kw)
    except ValueError:
        return "Capacidade deve ser numérica", 400

    consumo_medio_kW = round(capacidade_kw * 0.78, 2)
    horas_ano = 8760
    energia_total_kWh = int(round(consumo_medio_kW * horas_ano))
    energia_ti_kWh = int(round(energia_total_kWh * 0.69))
    energia_renovavel_kWh = int(round(energia_total_kWh * 0.40))
    fator_emissao = 0.07
    emissao_CO2_kg = int(round(energia_total_kWh * fator_emissao))
    
    fator_wue_ideal = 1.05 
    agua_consumida_L = int(round(energia_ti_kWh * fator_wue_ideal))
    

    carriers = [c.strip() for c in carriers_raw.split(",")] if carriers_raw else []

    novo_dc = {
        "codigo": codigo,
        "nome": nome,
        "localizacao": {
            "endereco": endereco,
            "latitude": latitude or "",
            "longitude": longitude or "",
        },
        "operacao": {
            "proprietario": proprietario,
            "tipo": tipo or "Colocation",
            "data_inicio": data_inicio or datetime.date.today().isoformat(),
            "status": status or "Planejamento",
            "sla_disponibilidade": sla or "99.00%"
        },
        "infraestrutura": {
            "area_total_m2": str(int(capacidade_kw * 1.6)),
            "area_util_m2": str(int(capacidade_kw * 1.6 * 0.65)),
            "num_racks": str(int(max(1, round(capacidade_kw / 10)))),
            "piso_elevado": True,
            "redundancia_energia": "N+1",
            "redundancia_climatizacao": "N+1"
        },
        "energia": {
            "alimentacao_principal": "",
            "capacidade_total_kW": str(int(capacidade_kw)),
            "consumo_medio_kW": str(consumo_medio_kW),
            "renovavel_kWh": str(energia_renovavel_kWh),
            "fator_emissao_kgCO2_kWh": str(fator_emissao),
            "fonte_fator": "ONS 2025",
            "ups": {
                "tipo": "Online Dupla Conversão",
                "fabricante": "APC",
                "modelo": "Symmetra PX",
                "autonomia_min": "15",
                "quantidade": "2"
            },
            "geradores": {
                "fabricante": "Cummins",
                "quantidade": "1",
                "autonomia_horas": "8"
            },
            "PUE": "",
            "DCiE": "",
            "WUE": "",
            "CUE": ""
        },
        "climatizacao": {
            "tipo": clima_tipo or "CRAC + Free Cooling",
            "capacidade_total_kW": str(int(capacidade_kw * 1.05)),
            "temperatura_media_C": "",
            "umidade_relativa": ""
        },
        "rede": {
            "carriers": carriers,
            "uplink_total_Gbps": str(uplink_total_Gbps or ""),
            "topologia": ""
        },
        "seguranca": {
            "fisica": {
                "biometria": True,
                "cftv": True,
                "retencao_imagens_dias": "90",
                "supressao_incendio": "FM200"
            },
            "logica": {}
        },
        "monitoramento": {
            "sistema": "Zabbix",
            "metricas": ["CPU", "Energia", "Temperatura", "Rede"],
            "alertas_email": True
        },
        "backup_e_DR": {},
        "metricas_ambientais": {
            "periodo": {
                "inicio": f"{datetime.date.today().year}-01-01",
                "fim": f"{datetime.date.today().year}-12-31"
            },
            "energia_total_kWh": str(energia_total_kWh),
            "energia_ti_kWh": str(energia_ti_kWh),
            "energia_renovavel_kWh": str(energia_renovavel_kWh),
            "agua_consumida_L": str(agua_consumida_L),
            "reuso_percentual": "0",
            "emissao_CO2_kg": str(emissao_CO2_kg),
            "fator_emissao_kgCO2_kWh": str(fator_emissao),
            "fonte_dado": ["estimado"],
            "tipo_calculo_emissao": "estimado"
        },
        "indicadores": {
            "pue": "",
            "cue": "",
            "wue": "",
            "dcie": "",
            "status": status or "Planejamento"
        }
    }

    r_pue = calcular_pue(novo_dc["metricas_ambientais"]["energia_total_kWh"], novo_dc["metricas_ambientais"]["energia_ti_kWh"])
    r_cue = calcular_cue(novo_dc["metricas_ambientais"]["emissao_CO2_kg"], novo_dc["metricas_ambientais"]["energia_ti_kWh"])
    r_dcie = calcular_dcie(novo_dc["metricas_ambientais"]["energia_total_kWh"], novo_dc["metricas_ambientais"]["energia_ti_kWh"])
    r_wue = calcular_wue(novo_dc["metricas_ambientais"]["agua_consumida_L"], novo_dc["metricas_ambientais"]["energia_ti_kWh"])

    if "pue" in r_pue: novo_dc["indicadores"]["pue"] = r_pue["pue"]
    if "cue" in r_cue: novo_dc["indicadores"]["cue"] = r_cue["cue"]
    if "dcie" in r_dcie: novo_dc["indicadores"]["dcie"] = r_dcie["dcie"]
    if "wue" in r_wue: novo_dc["indicadores"]["wue"] = r_wue["wue"]

    db.adicionar_datacenter(novo_dc)

    return redirect(url_for("homepage"))

@app.route("/datacenter/deletar/<int:id>", methods=["POST"])
def deletar(id):
    db.deletar_datacenter(id)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)