# FastAPI Persona CRUD (MySQL por defecto)

Proyecto de demostración con FastAPI + SQLAlchemy y estructura MVC para un CRUD de `Persona`. Usa MySQL por defecto y permite apuntar a otra base SQL mediante la variable de entorno `DATABASE_URL` (configurable en `.env`).

## Requisitos

- Python 3.10+ (recomendado 3.11)

## Instalación y ejecución

1. Crear entorno virtual e instalar dependencias:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Configurar variables de entorno:
   ```bash
   cp .env.example .env
   # Edita .env con tus credenciales de MySQL
   # Por defecto: DATABASE_URL=mysql+pymysql://user:password@localhost:3306/fastapi_demo
   ```

3. Ejecutar el servidor:
   ```bash
   uvicorn app.main:app --reload
   ```

4. Documentación interactiva:
   - Swagger UI: <http://localhost:8000/docs>
   - ReDoc: <http://localhost:8000/redoc>

## Conexión a otras bases de datos

Edita `DATABASE_URL` en `.env`.
- MySQL: `mysql+pymysql://user:password@localhost:3306/mydb`

> Nota: Instala el driver correspondiente (psycopg2, PyMySQL, pyodbc, etc.).

## Ejemplo de `.env` (MySQL local)

```env
DATABASE_URL=mysql+pymysql://usuario:contraseña@localhost:3306/nombre_basedatos
```

## Endpoints principales

- `GET /health` → estado del servicio
- `POST /personas` → crear persona
- `GET /personas` → listar personas (`skip`, `limit`)
- `GET /personas/{id}` → obtener persona por ID
- `PUT /personas/{id}` → actualizar (parcial) persona
- `DELETE /personas/{id}` → eliminar persona

# Responsabilidades — María Elizabeth Gómez Urrea


| Integrante | Puntos del laboratorio | Responsabilidad | Rama | Endpoints |
|------------|------------------------|-----------------|------|-----------|
| María Elizabeth Gómez Urrea | Puntos 3 y 5 | Búsqueda, proyección y bulk| `feature/busqueda-bulk` | `GET /personas/buscar/{termino}`, `GET /personas/reporte/activos`, `PATCH /personas/bulk/desactivar` |
### Endpoints de Elizabeth

#### GET /personas/buscar/{termino}
Busca un término de forma general en los campos `first_name`, `last_name`  o `email` utilizando el operador lógico OR.

Validación: Si no se encuentran coincidencias en la base de datos, no debe fallar; simplemente responde un arreglo vacío [] con un estado 200 OK.

Response 200 OK (Con resultados):
```text
[
  {
    "id": 5,
    "first_name": "Sofía",
    "last_name": "Lopez",
    "email": "sofia.lopez@gmail.com",
    "phone": "+57 3123456789",
    "birth_date": "1998-12-05",
    "is_active": true,
    "notes": "Estudiante de analítica"
  }
]
````
Response 200 OK (Sin resultados):

```text
[]
```
#### GET /personas/reporte/activos
Genera un listado filtrado únicamente con aquellos usuarios que se encuentran activos (is_active = true).

Proyección: Para optimizar la transferencia de datos, la respuesta se limita estrictamente a proyectar cuatro campos específicos: id, email, phone e is_active.

Response 200 OK:

```text 
[
  {
    "id": 3,
    "email": "felipe.villa@outlook.com",
    "phone": "+57 3001234567",
    "is_active": true
  },
  {
    "id": 7,
    "email": "elizabeth.gomez@gmail.com",
    "phone": null,
    "is_active": true
  }
]
````
####  PATCH /personas/bulk/desactivar
Recibe un listado de identificadores numéricos para desactivar de forma masiva el estado de las personas (is_active = false).

Validación: La lista de IDs enviada en el cuerpo de la petición no puede estar vacía y debe contener un máximo de 100 elementos; de lo contrario, responde un 400 Bad Request. Los IDs que no existan en la base de datos no detienen la transacción.

Request:
```text 
{
  "ids": [3, 7, 14, 999]
}
```
Response 200 OK:
```text 
{
  "message": "Operación completada.",
  "desactivados": [3, 7, 14],
  "no_encontrados": [999],
  "total_desactivados": 3
}
```
### Esquemas (JSON)

- Crear:
  ```json
  {
    "first_name": "Juan",
    "last_name": "Pérez",
    "email": "juan.perez@example.com",
    "phone": "+57 3000000000",
    "birth_date": "1990-05-20",
    "is_active": true,
    "notes": "Cliente frecuente"
  }
  ```

- Actualizar (parcial):
  ```json
  {
    "email": "juan.perez2@example.com",
    "notes": "Actualizado"
  }
  ```

## Colección de Postman

Importa `FastAPI-CRUD-Demo.postman_collection.json` en Postman. Variables:

- `base_url` (por defecto `http://localhost:8000`)
- `persona_id` (por defecto `1`)

## Notas

- Las tablas se crean automáticamente al iniciar (solo con fines de demo).
- Asegúrate de crear la base de datos en MySQL y de que el usuario tenga permisos (por ejemplo, `CREATE DATABASE fastapi_demo;`).

## Estructura MVC

- `app/models/` → modelos SQLAlchemy (por ejemplo, `persona.py`).
- `app/views/` → esquemas Pydantic (por ejemplo, `persona.py`).
- `app/controllers/` → routers/controladores FastAPI (por ejemplo, `persona_controller.py`).

## Pruebas rápidas (curl)

```bash
# Health
curl -s http://127.0.0.1:8000/health

# Crear persona
curl -s -X POST http://127.0.0.1:8000/personas \
  -H 'Content-Type: application/json' \
  -d '{
    "first_name":"Juan",
    "last_name":"Perez",
    "email":"juan.perez@example.com",
    "phone":"+57 3000000000",
    "birth_date":"1990-05-20",
    "is_active":true,
    "notes":"Cliente frecuente"
  }'

# Listar
curl -s http://127.0.0.1:8000/personas

# Obtener por ID
curl -s http://127.0.0.1:8000/personas/1

# Actualizar parcial
curl -s -X PUT http://127.0.0.1:8000/personas/1 \
  -H 'Content-Type: application/json' \
  -d '{"email":"juan.perez2@example.com","notes":"Actualizado"}'

# Eliminar
curl -s -X DELETE http://127.0.0.1:8000/personas/1 -i

## Detener el servidor

- Si lo iniciaste en la misma terminal: usa `CTRL+C`.
- Si corre en background, puedes cerrar esa terminal o matar el proceso de uvicorn (`pkill -f uvicorn`).
