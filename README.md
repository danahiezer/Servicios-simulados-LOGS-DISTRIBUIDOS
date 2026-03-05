# Logs Distribuidos 🪵

Proyecto para aprender como funciona un sistema de logging distribuido.
La idea es que varios servicios simulados generen logs falsos y los envíen a un servidor central que los guarda en una base de datos.

---

## ¿Qué hace este proyecto?

- Simula varios servicios (auth, pagos, inventario) generando logs falsos
- Los envía a un servidor central con autenticación por token
- El servidor los guarda en PostgreSQL
- Podés consultar los logs con filtros de fecha

---

## Archivos

- `logsServer.py` — el servidor central hecho con FastAPI
- `Service.py` — los servicios simulados que generan y envían logs
- `DBlogs.session.sql` — el script SQL para crear la tabla en PostgreSQL

---

## Tecnologías usadas

- Python
- FastAPI — framework para crear el servidor
- psycopg2 — para conectar Python con PostgreSQL
- PostgreSQL — base de datos donde se guardan los logs
- requests — para enviar los logs al servidor

---

## Instalación

1. Cloná el repositorio y creá un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate
```

2. Instalá las dependencias:
```bash
pip install fastapi uvicorn psycopg2-binary requests
```

3. Creá la base de datos en PostgreSQL y ejecutá el script `DBlogs.session.sql` para crear la tabla.

4. Cambiá los datos de conexión en `logsServer.py`:
```python
DBdata = {
    "host":     "localhost",
    "dbname":   "dblogs",
    "user":     "postgres",
    "password": "tu_contraseña"
}
```

---

## Cómo correrlo

**1. Arrancá el servidor:**
```bash
uvicorn logsServer:app --reload
```

**2. En otra terminal, corré los servicios simulados:**
```bash
python Service.py
```

---

## Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/logs` | Recibe y guarda un log |
| GET | `/logs` | Consulta logs con filtros opcionales |

Para probar los endpoints podés usar Thunder Client en VSCode o Postman.

---

## Autenticación

Cada servicio tiene su propio token. Se envía en el header de cada request:

```
Authorization: Token token-autenticacion
```

| Servicio | Token |
|----------|-------|
| auth-service | `token-autenticacion` |
| payment-service | `token-de-pago` |
| inventario-service | `token-de-inventario` |

Si el token es inválido el servidor responde:
```json
{"detail": "token invalido"}
```

---

## Filtros disponibles en GET /logs

| Parámetro | Descripción |
|-----------|-------------|
| `timestamp_start` | Logs desde esta fecha |
| `timestamp_end` | Logs hasta esta fecha |
| `received_at_start` | Recibidos desde esta fecha |
| `received_at_end` | Recibidos hasta esta fecha |

Ejemplo:
```
GET /logs?timestamp_start=2024-01-15T00:00:00&timestamp_end=2024-01-15T23:59:59
```

---

## Lo que aprendí haciendo este proyecto

- Cómo crear una API REST con FastAPI
- Cómo conectar Python con PostgreSQL usando psycopg2
- Cómo validar datos con Pydantic
- Cómo funciona la autenticación con tokens
- Cómo construir queries dinámicas con filtros opcionales
- Cómo enviar requests HTTP con la librería requests