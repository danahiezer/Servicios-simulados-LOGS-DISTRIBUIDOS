from fastapi import FastAPI,Depends,Query
from pydantic import BaseModel
from typing import Optional
import psycopg2
import psycopg2.extras

DBdata = {
    "host":"localhost",
    "dbname":"dblogs",
    "user":"postgres",
    "password":"dan"
}
app = FastAPI()

def getDB():
    conn = psycopg2.connect(**DBdata)
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        yield conn,cur
    finally:
        cur.close()
        conn.close()

class LogEntry(BaseModel):
    timestamp: str
    service:   str
    severity:  str
    message:   str

@app.get("/logs")
def optenerDatos(db= Depends(getDB),
                timestamp_start: Optional[str]= Query(default=None),
                timestamp_end: Optional[str]= Query(default=None),
                received_at_start: Optional[str]= Query(default=None),
                received_at_end: Optional[str]= Query(default=None)):
    conn,cur = db
    consult = "SELECT * FROM logs WHERE 1=1"
    datosLogs = []
    if timestamp_start:
        consult += " AND timestamp >= %s"
        datosLogs.append(timestamp_start)

    if timestamp_end:
        consult += " AND timestamp <= %s"
        datosLogs.append(timestamp_end)
    
    if received_at_start:
        consult += " AND received_at >= %s"
        datosLogs.append(received_at_start)

    if received_at_end:
        consult += " AND received_at <= %s"
        datosLogs.append(received_at_end)

    cur.execute(consult,datosLogs)
    logs = cur.fetchall()
    return logs
    

@app.post("/logs")
def recibir_log(log: LogEntry, db = Depends(getDB)):
    conn,cur = db
    cur.execute("INSERT INTO logs(timestamp,service,severity,message) VALUES (%s,%s,%s,%s)"
                ,(log.timestamp,log.service,log.severity,log.message))
    conn.commit()
    print(f"Log recibido: {log}")
    return {"status": "ok", "log_recibido": log}
