def calcular_pue(energia_total, energia_ti):
    try:
        energia_total = float(str(energia_total).replace('.', '').replace(',', '.'))
        energia_ti = float(str(energia_ti).replace('.', '').replace(',', '.'))

        if energia_ti == 0:
             return {"erro": "A energia de TI não pode ser zero para calcular o PUE."}

        pue = energia_total / energia_ti
      
        if pue <= 1.5:
            status = "Ideal"
        elif 1.5 < pue <= 2.0:
            status = "Aceitável"
        elif 2.0 < pue <= 3.0:
            status = "Preocupante"
        else:
            status = "Alarmante"

        return {
            "pue": round(pue, 2),
            "status": status
        }

    except ValueError:
        return {"erro": "Valor de energia inválido. Certifique-se de inserir apenas números."}
    except Exception as e:
         return {"erro": f"Erro inesperado no cálculo do PUE: {e}"}


def calcular_cue(emissao_total_co2, energia_ti):
    try:
        emissao_total_co2 = float(str(emissao_total_co2).replace('.', '').replace(',', '.'))
        energia_ti = float(str(energia_ti).replace('.', '').replace(',', '.'))

        if energia_ti == 0:
             return {"erro": "A energia de TI não pode ser zero para calcular o CUE."}

        cue = emissao_total_co2 / energia_ti
        
        if cue <= 0.5:
            status = "Ideal"
        elif 0.5 < cue <= 1.0:
            status = "Aceitável"
        elif 1.0 < cue <= 2.0:
            status = "Preocupante"
        else:
            status = "Alarmante"

        return {
            "cue": round(cue, 2),
            "status": status
        }
    except ValueError:
        return {"erro": "Valor inválido. Certifique-se de inserir apenas números."}
    except Exception as e:
         return {"erro": f"Erro inesperado no cálculo do CUE: {e}"}


def calcular_dcie(energia_total, energia_ti):
    try:
        energia_total = float(str(energia_total).replace('.', '').replace(',', '.'))
        energia_ti = float(str(energia_ti).replace('.', '').replace(',', '.'))

        if energia_total == 0:
             return {"erro": "A energia total não pode ser zero para calcular o DCiE."}

        dcie = (energia_ti / energia_total) * 100
        
        if dcie >= 70:
            status = "Ideal"
        elif 50 <= dcie < 70:
            status = "Aceitável"
        elif 30 <= dcie < 50:
            status = "Preocupante"
        else:
            status = "Alarmante"

        return {
            "dcie": round(dcie, 2),
            "status": status
        }
    except ValueError:
        return {"erro": "Valor inválido. Certifique-se de inserir apenas números."}
    except Exception as e:
         return {"erro": f"Erro inesperado no cálculo do DCiE: {e}"}


def calcular_wue(volume_agua_utilizada, energia_ti):
    try:
        volume_agua_utilizada = float(str(volume_agua_utilizada).replace('.', '').replace(',', '.'))
        energia_ti = float(str(energia_ti).replace('.', '').replace(',', '.'))

        if energia_ti == 0:
             return {"erro": "A energia de TI não pode ser zero para calcular o WUE."}

        wue = volume_agua_utilizada / energia_ti
        
        if wue <= 1.0:
            status = "Ideal"
        elif 1.0 < wue <= 2.0:
            status = "Aceitável"
        elif 2.0 < wue <= 3.0:
            status = "Preocupante"
        else:
             status = "Alarmante"

        return {
            "wue": round(wue, 2),
            "status": status
        }
    except ValueError:
        return {"erro": "Valor inválido. Certifique-se de inserir apenas números."}
    except Exception as e:
         return {"erro": f"Erro inesperado no cálculo do WUE: {e}"}


def limitar_angulo(a):
    return max(-90, min(90, a))

def calcular_angulo_pue(pue):
    if pue <= 1.0:
        return -90
    if pue >= 4.0:
        return 90
    
    angulo = -90 + ((pue - 1.0) / 3.0) * 180
    return limitar_angulo(angulo)

def calcular_angulo_cue(cue, v_max=1.0): 
    if cue <= 0:
        return -90
    if cue >= v_max:
        return 90
    angulo = -90 + (cue / v_max) * 180
    return limitar_angulo(angulo)

def calcular_angulo_dcie(dcie, v_min=0, v_max=100):
    if dcie <= v_min:
        return -90
    if dcie >= v_max:
        return 90
    angulo = -90 + ((dcie - v_min) / (v_max - v_min)) * 180
    return limitar_angulo(angulo)

def calcular_angulo_wue(wue, v_max=2.0): 
    if wue <= 0:
        return -90
    if wue >= v_max:
        return 90
    angulo = -90 + (wue / v_max) * 180
    return limitar_angulo(angulo)