import requests
from datetime import datetime,timezone
import random


servicios = [
    {"nombre": "auth-service",      "token": "token-autenticacion"},
    {"nombre": "payment-service",   "token": "token-de-pago"},
    {"nombre": "inventario-service","token": "token-de-inventario"},
]


def generaLogs():
    service = random.choice(servicios)
    logs = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": service["nombre"],
        "severity": random.choice(["ERROR","WARNING","INFO","DEBUG"]),
        "message": "cualquiera"
    }

    return logs, servicios["token"]