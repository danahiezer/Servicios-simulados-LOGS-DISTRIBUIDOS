from fastapi import FastAPI,Depends,Query,Header,HTTPException
from pydantic import BaseModel
from typing import Optional
import psycopg2
import psycopg2.extras

# dicc. conn los datos de mi data base
DBdata = {
    "host":"localhost",
    "dbname":"dblogs",
    "user":"postgres",
    "password":"dan"
}
# dicc con algunos tokens para mi hedear y validacion
tokens = {
    "token-autenticacion":      "auth-service",
    "token-de-pago":           "payment-service",
    "token-de-inventario":     "inventory-service",
}

app = FastAPI() # creacion de servidor web

def verificaTokens(authorization: str = Header(...)):

    partes = authorization.split(" ") # separa por el espacio y devuelve como lista

    if len(partes) != 2 or partes[0] != "Token": # verifica que si no hay dos parte y que partes[0] es distinto a token devuelve token invalido
        raise HTTPException(status_code=401, detail="token invalido")
    
    if partes[1] not in tokens: # si la parte[1] no es parte de la lista tokens dvuelve token ivalido
        raise HTTPException(status_code=401, detail="token invalido")
    
    return tokens[partes[1]] # devuelve los tokens

#funcion para la conexion de base de datos
def getDB():
    conn = psycopg2.connect(**DBdata) #conecta con la base de datos
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)# con esto ejecuta las consultas y hace que los resultados del select lleguen como dicc.
    try:
        yield conn,cur # yield solo pausa y el endpoint usa la conexion, cuando termina la funcion continua a finally -> Esta funcion abre una conexion para cada request para que no se crucen o "pisen"
    finally:
        cur.close()
        conn.close()

# con esta clase y la libreria de pydantic(baseModel) defino como debe verse el JSON que llega
class LogEntry(BaseModel):
    timestamp: str
    service:   str
    severity:  str
    message:   str

# con el metodo get recivo los datos del log que estan en mi base de datos
@app.get("/logs") 
def optenerDatos(db= Depends(getDB),servicio= Depends(verificaTokens),
                timestamp_start: Optional[str]= Query(default=None),
                timestamp_end: Optional[str]= Query(default=None),     # ----> aca estoy declarando los parametros para los filtros dinamicos (por fecha) 
                received_at_start: Optional[str]= Query(default=None),
                received_at_end: Optional[str]= Query(default=None)):
    conn,cur = db
    consult = "SELECT * FROM logs WHERE 1=1" # ---> trae todos los logs y 1=1 es verdadero no filtra nada pero me deja usar AND para filtrar luego
    datosLogs = []       # -------> en esta lista se agregan los valores de los filtros 
    if timestamp_start:
        consult += " AND timestamp >= %s"
        datosLogs.append(timestamp_start)

    if timestamp_end:
        consult += " AND timestamp <= %s"
        datosLogs.append(timestamp_end)       # -----> estos son los filtros con los que se guardan en la base de datos 
    
    if received_at_start:
        consult += " AND received_at >= %s"
        datosLogs.append(received_at_start)

    if received_at_end:
        consult += " AND received_at <= %s"
        datosLogs.append(received_at_end)

    cur.execute(consult,datosLogs)
    logs = cur.fetchall()
    return logs
    
# metodo  post envia datos de mi log a la base de datos 
@app.post("/logs")
def recibir_log(log: LogEntry, db = Depends(getDB), servicio=Depends(verificaTokens)):  # ---> declaro dependencias
    conn,cur = db
    cur.execute("INSERT INTO logs(timestamp,service,severity,message) VALUES (%s,%s,%s,%s)" 
                ,(log.timestamp,log.service,log.severity,log.message))  # ----> inserto los datos de mi log en la base de datos
    conn.commit()
    print(f"Log recibido: {log}")
    return {"status": "ok", "log_recibido": log}
