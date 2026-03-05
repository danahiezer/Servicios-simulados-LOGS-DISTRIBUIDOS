import requests
from datetime import datetime,timezone
import random

# lista de servicios, con nombres del servicio y tokens
servicios = [
    {"nombre": "auth-service",      "token": "token-autenticacion"},
    {"nombre": "payment-service",   "token": "token-de-pago"},
    {"nombre": "inventario-service","token": "token-de-inventario"},
]

# funcion para generar esos logs random
def generaLogs():
    service = random.choice(servicios)
    logs = {
        "timestamp": datetime.now(timezone.utc).isoformat(), # --> obtiene el tiempo con la zona horaria y lo  muestra en formato iso
        "service": service["nombre"],
        "severity": random.choice(["ERROR","WARNING","INFO","DEBUG"]),
        "message": "cualquiera"
    }

    return logs, service["token"]
# funcion para enviar los logs randoms
def enviarLogs(log,token):
    headers = {
        "Authorization": f"Token {token}" # --> header con el token 
    }

    respuesta = requests.post(
        "http://localhost:8000/logs", # --> respuesta (se envia el log) con la url el json del log y su header
        json = {"logs": [log]},
        headers = headers
    )

    print(f"status: {respuesta.status_code}") # --> muestra el estado de la respuesta 

if __name__ == "__main__":

    log,token = generaLogs() # --> codigo principal con sus parametros
    enviarLogs(log,token)
