def calcular_pue(energia_total, energia_ti):
   
    try:
        energia_total = float(energia_total.replace('.', '').replace(',', '.'))
        energia_ti = float(energia_ti.replace('.', '').replace(',', '.'))

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
        return {"erro": "Valor inválido. Certifique-se de inserir apenas números."}

def calcular_cue(emissao_total_co2, energia_ti):
  
     emissao_total_co2 = float(emissao_total_co2.replace('.', '').replace(',', '.'))
     energia_ti = float(energia_ti.replace('.', '').replace(',', '.'))

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


def calcular_dcie(energia_total, energia_ti):
  
     energia_total = float(energia_total.replace('.', '').replace(',', '.'))
     energia_ti = float(energia_ti.replace('.', '').replace(',', '.'))

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


def calcular_wue(volume_agua_utilizada, energia_ti):
  
     volume_agua_utilizada = float(volume_agua_utilizada.replace('.', '').replace(',', '.'))
     energia_ti = float(energia_ti.replace('.', '').replace(',', '.'))

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