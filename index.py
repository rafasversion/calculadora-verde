import json
from flask import Flask, request, render_template
from calculador import calcular_pue
from calculador import calcular_cue
from calculador import calcular_dcie
from calculador import calcular_wue

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/metricas")
def metricas():
    return render_template("metricas.html")

@app.route("/datacenter")
def datacenter():
    with open("datacenters.json", "r", encoding="utf-8") as f:
        dados = json.load(f)

    for dc in dados["datacenters"]:
        m = dc["metricas_ambientais"]
        energia_total = m["energia_total_kWh"]
        energia_ti = m["energia_ti_kWh"]
        emissao = m["emissao_CO2_kg"]
        agua = m["agua_consumida_L"]

        dc["energia"]["PUE"] = calcular_pue(energia_total, energia_ti)["pue"]
        dc["energia"]["DCiE"] = calcular_dcie(energia_total, energia_ti)["dcie"]
        dc["energia"]["CUE"] = calcular_cue(emissao, energia_ti)["cue"]
        dc["energia"]["WUE"] = calcular_wue(agua, energia_ti)["wue"]

    return render_template("datacenter.html", datacenters=dados["datacenters"])

@app.route("/calcular", methods=["POST"])
def calcular():
    energia_total = request.form.get("energia_total")
    energia_ti = request.form.get("energia_equipamentos")
    emissao_total_co2 = request.form.get("emissao_total_co2")
    volume_agua_utilizada = request.form.get("volume_agua_utilizada")

    resultado_pue = calcular_pue(energia_total, energia_ti)

    if "erro" in resultado_pue:
        mensagem_pue = f"{resultado_pue['erro']}"
        angulo_pue = 0 
    else:
        mensagem_pue = (
            f"<strong>PUE:</strong> {resultado_pue['pue']:.2f}<br>"
            f"<strong>Status:</strong> {resultado_pue['status']}"
            )
        pue = resultado_pue["pue"]

        if pue < 1:
            angulo_pue = -90
        elif pue > 4:
            angulo_pue = 90
        else:
      
            angulo_pue = -90 + (pue - 1) * 60

  
        angulo_pue = max(-90, min(90, angulo_pue))

  # cue
    resultado_cue = calcular_cue(emissao_total_co2, energia_ti)

    if "erro" in resultado_cue:
        mensagem_cue = f"{resultado_cue['erro']}"
        angulo_cue = 0 
    else:
        mensagem_cue = (
            f"<strong>CUE:</strong> {resultado_cue['cue']:.2f}<br>"
            f"<strong>Status:</strong> {resultado_cue['status']}"
        )

        cue = resultado_cue["cue"]

        if cue < 1:
            angulo_cue = -90
        elif pue > 4:
            angulo_cue = 90
        else:
      
            angulo_cue = -90 + (cue - 1) * 60

  
        angulo_cue = max(-90, min(90, angulo_cue))

   # dcie
    resultado_dcie = calcular_dcie(energia_total, energia_ti)

    if "erro" in resultado_dcie:
        mensagem_dcie = f"{resultado_dcie['erro']}"
        angulo_dcie = 0 
    else:
        mensagem_dcie = (
            f"<strong>DCiE:</strong> {resultado_dcie['dcie']:.2f}<br>"
            f"<strong>Status:</strong> {resultado_dcie['status']}"
            )

        dcie = resultado_dcie["dcie"]

        if dcie < 1:
            angulo_dcie = -90
        elif pue > 4:
            angulo_dcie = 90
        else:
      
            angulo_dcie = -90 + (dcie - 1) * 60

  
        angulo_dcie = max(-90, min(90, angulo_dcie))

# wue

    resultado_wue = calcular_wue(volume_agua_utilizada, energia_ti)

    if "erro" in resultado_wue:
        mensagem_wue = f"{resultado_wue['erro']}"
        angulo_wue = 0 
    else:
        mensagem_wue = (
            f"<strong>WUE:</strong> {resultado_wue['wue']:.2f}<br>"
            f"<strong>Status:</strong> {resultado_wue['status']}"
            )

        wue = resultado_wue["wue"]

        if wue < 1:
            angulo_wue = -90
        elif wue > 4:
            angulo_wue = 90
        else:
      
            angulo_wue = -90 + (wue - 1) * 60

  
        angulo_wue = max(-90, min(90, angulo_wue))

    return render_template("homepage.html", resultado_pue=mensagem_pue, angulo_pue=angulo_pue, resultado_cue=mensagem_cue, angulo_cue=angulo_cue, resultado_dcie=mensagem_dcie, angulo_dcie=angulo_dcie, resultado_wue=mensagem_wue, angulo_wue=angulo_wue)


if __name__ == "__main__":
    app.run(debug=True)
