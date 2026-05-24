# README.md - Laboratorio 1 API REST con FastAPI

## Contexto del proyecto

Esta aplicacion es una API REST construida con FastAPI, SQLAlchemy y MySQL para administrar registros de personas. El proyecto base ya incluye un CRUD sobre el recurso `Persona`, y en este laboratorio se extendio con 9 endpoints nuevos orientados a carga masiva de datos, analitica SQL, busqueda, filtros por fecha, operaciones bulk y exportacion CSV.

La aplicacion sirve para:

- Crear, listar, consultar, actualizar y eliminar personas.
- Poblar la base de datos con datos realistas usando Faker.
- Ejecutar consultas analiticas sobre correos, edades y fechas de nacimiento.
- Buscar personas por nombre, apellido o correo.
- Generar reportes reducidos de personas activas.
- Desactivar multiples personas en una sola operacion.
- Exportar los registros de la tabla `personas` en formato CSV.

El modelo `Persona` contiene los campos:

- `id`
- `first_name`
- `last_name`
- `email`
- `phone`
- `birth_date`
- `is_active`
- `notes`
- `created_at`

## Tecnologias usadas

- Python 3.10+
- FastAPI
- Uvicorn
- SQLAlchemy
- MySQL
- PyMySQL
- Pydantic
- Faker
- Postman

La arquitectura mantiene una separacion tipo MVC:

- `models/`: definicion de tablas con SQLAlchemy.
- `views/`: schemas de entrada y salida con Pydantic.
- `controllers/`: rutas HTTP de FastAPI.
- `services/`: logica de negocio y consultas a base de datos.

## Requisitos previos

Antes de ejecutar el proyecto debes tener instalado:

- Python 3.10 o superior.
- MySQL Server activo.
- Postman, si quieres importar y probar la coleccion.

Tambien debes tener creada una base de datos en MySQL. Por ejemplo:

```sql
CREATE DATABASE fastapi_demo;
```

## Ejecucion paso a paso

### 1. Realizar `git clone` al repositorio

```powershell
git clone https://github.com/f-villa4/CRUD_FastAPI.git
```


### 2. Crear el entorno virtual

```powershell
python -m venv .venv
```

### 3. Activar el entorno virtual

En PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activacion por politicas de ejecucion, puedes usar:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Luego intenta activar el entorno virtual nuevamente.

### 4. Instalar dependencias

```powershell
pip install -r requirements.txt
```

El archivo `requirements.txt` incluye las dependencias necesarias para FastAPI, SQLAlchemy, MySQL y Faker.

### 5. Configurar la conexion a MySQL

Crea un archivo `.env` en la raiz del proyecto o edita el existente:

```env
DATABASE_URL=mysql+pymysql://usuario:contrasena@localhost:3306/fastapi_demo
```

Ajusta `usuario`, `contrasena`, host, puerto y nombre de base de datos segun tu instalacion local.

### 6. Ejecutar el servidor

```powershell
uvicorn app.main:app --reload
```

### 7. Abrir la documentacion interactiva

Con el servidor activo, abre:

- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>

### 8. Probar el estado de la API

En PowerShell:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/health" -Method GET
```

Respuesta esperada:

```json
{
  "status": "ok"
}
```

## Coleccion de Postman

El archivo principal de Postman es:

```text
FastAPI-CRUD-Demo.postman_collection.json
```

Para usarlo:

1. Abre Postman.
2. Haz clic en `Import`.
3. Selecciona `FastAPI-CRUD-Demo.postman_collection.json`.
4. Verifica que la variable `base_url` tenga este valor:

```text
http://localhost:8000
```

La coleccion debe incluir las peticiones del CRUD original y las 9 peticiones nuevas del laboratorio.

## Endpoints CRUD originales

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET | `/health` | Verifica que la API este activa. |
| POST | `/personas` | Crea una persona. |
| GET | `/personas` | Lista personas con paginacion. |
| GET | `/personas/{persona_id}` | Consulta una persona por ID. |
| PUT | `/personas/{persona_id}` | Actualiza parcialmente una persona. |
| DELETE | `/personas/{persona_id}` | Elimina una persona por ID. |

Ejemplo para crear una persona:

```json
{
  "first_name": "Juan",
  "last_name": "Perez",
  "email": "juan.perez@example.com",
  "phone": "+57 3000000000",
  "birth_date": "1990-05-20",
  "is_active": true,
  "notes": "Cliente frecuente"
}
```

## Desarrollo por integrante
De esta manera los integrantes desarrollaron el proyecto:

| Integrante | Rama | Responsabilidad | Endpoints |
|------------|------|-----------------|-----------|
| Felipe Villa Velasquez | `feature/masivas` | Operaciones masivas y exportacion CSV | `POST /personas/poblar`, `DELETE /personas/reset`, `GET /personas/exportar/csv` |
| Sofia Lopez Lopera | `feature/analitica-fechas` | Analitica SQL y filtros por fecha | `GET /personas/estadisticas/dominios`, `GET /personas/estadisticas/edad`, `GET /personas/cumpleanios/mes/{numero_mes}` |
| Maria Elizabeth Gomez Urrea | `feature/busqueda-bulk` | Busqueda, proyeccion y operaciones bulk | `GET /personas/buscar/{termino}`, `GET /personas/reporte/activos`, `PATCH /personas/bulk/desactivar` |

### Felipe Villa Velasquez - puntos 1 y 6

Felipe implemento las operaciones masivas y la exportacion de datos. Su desarrollo se concentra en generar datos de prueba realistas, reiniciar la tabla de personas y entregar los datos en formato CSV.

Endpoints:

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| POST | `/personas/poblar` | Recibe una cantidad y crea personas automaticamente con Faker. |
| DELETE | `/personas/reset` | Elimina todos los registros de la tabla `personas`. |
| GET | `/personas/exportar/csv` | Exporta todos los registros en formato CSV. |

Cambios principales:

- Agrego `Faker` a `requirements.txt`.
- Agrego los schemas `PoblarRequest`, `PoblarResponse` y `ResetResponse`.
- Creo el servicio `persona_masivas.py`.
- Implemento generacion de nombres, apellidos, correos con dominios reales, telefonos, fechas, estados y notas.
- Implemento la validacion de `cantidad` entre 1 y 1000.
- Implemento borrado total con retorno de `deleted_count`.
- Implemento exportacion CSV con `StreamingResponse`.

Ejemplo de `POST /personas/poblar`:

```json
{
  "cantidad": 50
}
```

Respuesta esperada:

```json
{
  "message": "50 usuarios creados exitosamente",
  "status": 201
}
```

### Sofia Lopez Lopera - puntos 2 y 4

Sofia implemento los endpoints de analitica y filtros por fecha. Su desarrollo permite comparar resultados de la API contra consultas SQL ejecutadas en DBeaver.

Endpoints:

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET | `/personas/estadisticas/dominios` | Agrupa personas por dominio de correo. |
| GET | `/personas/estadisticas/edad` | Calcula edad promedio, minima y maxima. |
| GET | `/personas/cumpleanios/mes/{numero_mes}` | Lista personas que cumplen anos en un mes especifico. |

Cambios principales:

- Agrego el schema `PersonaLabRead`.
- Creo el servicio `persona_analitica_fechas.py`.
- Implemento agrupacion por dominio usando la parte posterior al `@` del email.
- Implemento calculo de edades con funciones SQL sobre `birth_date`.
- Implemento filtro por mes usando funciones de fecha SQL.
- Agrego validacion para que `numero_mes` este entre 1 y 12.

Ejemplo de respuesta de `GET /personas/estadisticas/edad`:

```json
{
  "edad_promedio": 34,
  "edad_minima": 18,
  "edad_maxima": 85
}
```

Ejemplo de error para mes invalido:

```json
{
  "detail": "El mes debe ser un entero entre 1 y 12."
}
```

### Maria Elizabeth Gomez Urrea - puntos 3 y 5

Elizabeth implemento los endpoints de busqueda, reporte de activos y desactivacion masiva. Su desarrollo permite consultar personas por termino, generar una proyeccion reducida de usuarios activos y actualizar varios registros en una sola operacion.

Endpoints:

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET | `/personas/buscar/{termino}` | Busca el termino en `first_name`, `last_name` o `email`. |
| GET | `/personas/reporte/activos` | Retorna solo `id`, `email`, `phone` e `is_active` de usuarios activos. |
| PATCH | `/personas/bulk/desactivar` | Desactiva multiples personas por ID y reporta IDs no encontrados. |

Cambios principales:

- Agrego los schemas `PersonaActivaReport`, `BulkDesactivarRequest` y `BulkDesactivarResponse`.
- Creo el servicio `persona_busqueda_bulk.py`.
- Implemento busqueda con operador OR sobre nombre, apellido y correo.
- Implemento reporte de personas activas con proyeccion reducida.
- Implemento desactivacion masiva con lista de IDs.
- Agrego validacion para listas vacias o con mas de 100 IDs.
- Reporta IDs inexistentes sin fallar la operacion.

Ejemplo de `PATCH /personas/bulk/desactivar`:

```json
{
  "ids": [3, 7, 14, 999]
}
```

Respuesta esperada:

```json
{
  "message": "Operacion completada.",
  "desactivados": [3, 7, 14],
  "no_encontrados": [999],
  "total_desactivados": 3
}
```

## Validaciones recomendadas en DBeaver

Despues de ejecutar los endpoints, se recomienda contrastar con SQL:

```sql
SELECT COUNT(*) FROM personas;

SELECT SUBSTRING_INDEX(email, '@', -1) AS dominio, COUNT(*) AS cantidad
FROM personas
GROUP BY dominio;

SELECT
  AVG(TIMESTAMPDIFF(YEAR, birth_date, CURDATE())) AS edad_promedio,
  MIN(TIMESTAMPDIFF(YEAR, birth_date, CURDATE())) AS edad_minima,
  MAX(TIMESTAMPDIFF(YEAR, birth_date, CURDATE())) AS edad_maxima
FROM personas
WHERE birth_date IS NOT NULL;

SELECT *
FROM personas
WHERE MONTH(birth_date) = 12;

SELECT id, email, phone, is_active
FROM personas
WHERE is_active = 1;

SELECT id, is_active
FROM personas
WHERE id IN (3, 7, 14, 999);
```