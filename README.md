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

## Laboratorio 1 - Responsabilidades del equipo

| Integrante | Puntos del laboratorio | Responsabilidad | Rama | Endpoints |
|------------|------------------------|-----------------|------|-----------|
| Felipe Villa Velasquez | Puntos 1 y 6 | Operaciones masivas y exportacion CSV | `feature/masivas` | `POST /personas/poblar`, `DELETE /personas/reset`, `GET /personas/exportar/csv` |

### Endpoints de Felipe

#### `POST /personas/poblar`

Recibe una cantidad de registros y crea personas automaticamente usando Faker. El backend genera `first_name`, `last_name`, `email`, `phone`, `birth_date`, `is_active` y `notes`.

Validacion:

- `cantidad` debe estar entre 1 y 1000.
- Si `cantidad <= 0` o `cantidad > 1000`, responde `400 Bad Request`.

Request:

```json
{
  "cantidad": 50
}
```

Response `201 Created`:

```json
{
  "message": "50 usuarios creados exitosamente",
  "status": 201
}
```

#### `DELETE /personas/reset`

Elimina todos los registros de la tabla `personas` para reiniciar los datos del laboratorio.

Response `200 OK`:

```json
{
  "message": "Base de datos limpiada. Se eliminaron todos los registros.",
  "deleted_count": 150
}
```

#### `GET /personas/exportar/csv`

Exporta todos los registros de `personas` en formato CSV para descargar o abrir en Excel/Pandas.

Cabeceras esperadas:

- `Content-Type: text/csv`
- `Content-Disposition: attachment; filename="personas.csv"`

Columnas exportadas:

- `id`
- `first_name`
- `last_name`
- `email`
- `phone`
- `birth_date`
- `is_active`
- `notes`

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
```

# LABORATORIO 1 

# Implementación de Endpoints Analíticos y Filtros por Fecha — FastAPI Persona CRUD
## Autora
**Sofía Lopez Lopera**  
Rama de trabajo:
```bash
feature/analitica-fechas 
```
# Objetivo del desarrollo

la implementación de un módulo avanzado de análisis, consultas y filtrado de información por fechas dentro del sistema CRUD de Personas construido con FastAPI. Esta mejora buscó ampliar las capacidades funcionales de la API, permitiendo no solo realizar operaciones básicas de creación, consulta, actualización y eliminación de registros, sino también incorporar procesos analíticos y consultas especializadas orientadas al manejo eficiente de datos relacionados con usuarios y fechas importantes.

Durante el desarrollo se diseñaron e implementaron nuevos endpoints enfocados en la generación de estadísticas, validaciones y consultas dinámicas, garantizando una arquitectura organizada, escalable y fácil de mantener. Cada funcionalidad fue construida siguiendo buenas prácticas de desarrollo backend y separación de responsabilidades mediante arquitectura por capas.

Entre las principales funcionalidades implementadas se encuentran:

* Generación de estadísticas agrupadas por dominio de correo electrónico, permitiendo analizar la distribución de usuarios según proveedores de email como Gmail, Outlook, Yahoo, entre otros.
* Implementación de estadísticas de edad, realizando cálculos y agrupaciones sobre la información almacenada en la base de datos para obtener métricas relevantes relacionadas con rangos etarios de los usuarios registrados.
* Creación de consultas especializadas para la búsqueda de cumpleaños por mes, facilitando la obtención de registros filtrados según fechas específicas y permitiendo consultas dinámicas utilizando parámetros enviados desde la API.
* Desarrollo de validaciones robustas de parámetros de entrada, garantizando que los datos recibidos por los endpoints cumplan con los formatos y restricciones definidas previamente, reduciendo errores y mejorando la integridad de la información procesada.
* Implementación de manejo de errores HTTP mediante respuestas controladas y personalizadas, utilizando códigos de estado adecuados y mensajes descriptivos para facilitar la depuración y mejorar la experiencia del consumidor de la API.

Además, el desarrollo incluyó la organización completa del proyecto siguiendo una arquitectura por capas, permitiendo separar responsabilidades y mantener un código más limpio, reutilizable y escalable. La estructura implementada se dividió en los siguientes componentes:

* Views (Schemas): encargadas de definir las estructuras de validación y serialización de datos utilizando modelos Pydantic para controlar la información de entrada y salida de los endpoints.
* Services: responsables de contener toda la lógica de negocio y procesamiento de datos, centralizando cálculos, validaciones y reglas funcionales del sistema.
* Controllers: encargados de gestionar las rutas y endpoints de la API, recibiendo solicitudes HTTP y conectando las peticiones con los servicios correspondientes.

Adicionalmente, se realizaron pruebas funcionales de cada endpoint utilizando herramientas como Swagger UI y Thunder Client desde Visual Studio Code, verificando el correcto funcionamiento de las rutas, las respuestas HTTP y la integración completa entre controladores, servicios y esquemas.

Finalmente, este desarrollo permitió transformar el CRUD básico inicial en una API más robusta, organizada y orientada al análisis de información, incorporando funcionalidades reales utilizadas comúnmente en sistemas backend modernos construidos con FastAPI.

# Estructura modificada en Visual Studio Code

## Durante el desarrollo se trabajó sobre los siguientes archivos:
```
app/

├── controllers/

│   └── persona_controller.py

│

├── services/

│   └── persona_analitica_fechas.py   ← NUEVO

│

├── views/

│   └── persona.py
```
## 1. Modificación de Schemas (Views)

## Archivo modificado
```
app/views/persona.py
```
## ¿Qué se hizo?

Se agregó un nuevo schema encargado de validar y estructurar los datos utilizados en los nuevos endpoints del sistema. Este schema fue desarrollado con Pydantic para garantizar que la información recibida y enviada por la API cumpliera correctamente con los formatos y tipos de datos definidos.
```
PersonaLabRead
```
## ¿Por qué fue necesario?

El sistema ya contaba con schemas básicos para las operaciones CRUD de Personas, pero fue necesario agregar uno nuevo para soportar las validaciones y estructuras requeridas por los endpoints de análisis y filtros por fecha.
 ```
 PersonaRead
 ```
 pero este schema incluía:
 ```
 created_at
 ```
 para los endpoints analiticos relacionados con cumpleaños, este campo no era requerido dentro de esta respuesta. por esta razon, se optó por crear un schema más limpio y especializado,enfocado únicamente en la información necesaria para este tipo de consultas

 # Código implementado
 ```
 class PersonaLabRead(BaseModel):

    """Persona payload for lab endpoints (no created_at)."""

    id: int

    first_name: str

    last_name: str

    email: EmailStr

    phone: str | None

    birth_date: date | None

    is_active: bool

    notes: str | None

    model_config = {"from_attributes": True}
  ```
   ## Resultado

Ahora los endpoints analíticos pueden devolver únicamente la información relevante relacionada con consultas de cumpleaños y filtros por fecha, optimizando las respuestas de la API y facilitando búsquedas más precisas y organizadas según los parámetros enviados por el usuario.

# 2. Creación de Services Analíticos

## Archivo creado
```
app/services/persona_analitica_fechas.py
```
En esta parte lo que hacemos es crear un nuevo módulo de servicios especializado en:

* análisis de datos
* estadísticas
* consultas SQL avanzadas
* filtros por fecha

# Función 1 — Estadísticas por dominio

## Objetivo

Realizar el conteo y agrupación de personas registradas según el dominio de su correo electrónico, permitiendo generar estadísticas organizadas por proveedores de email como Gmail, Outlook, Yahoo, entre otros. Esta funcionalidad facilita el análisis de la distribución de usuarios dentro del sistema y permite obtener información útil para procesos de análisis y visualización de datos.

## código implementado
```
def estadisticas_dominios(db: Session) -> dict[str, int]:
```
## Lógica implementada

Se utilizó:
```
func.substring_index()
```
Ejemplo:
```
juan@gmail.com → gmail.com
```
Luego se aplicó:
```
GROUP BY

COUNT
```
para agrupar y contar resultados.

## Consulta SQL equivalente

```
SELECT SUBSTRING_INDEX(email, '@', -1) AS dominio,

       COUNT(*) AS cantidad

FROM personas

GROUP BY dominio;
```
## Resultado esperado
```
{

  "gmail.com": 10,

  "hotmail.com": 4

}
```

# Función 2 — Estadísticas de edad

## Objetivo

Calcular las principales métricas relacionadas con la edad de las personas registradas en el sistema, incluyendo la edad promedio, la edad mínima y la edad máxima. Este análisis permite obtener una visión general del rango etario de los usuarios, facilitando la interpretación de los datos y el apoyo en procesos de estadística y toma de decisiones dentro del sistema.

## Código implementado
```
def estadisticas_edad(db: Session) -> dict[str, Any]:
```

## Lógica implementada

Se utilizó:
```
TIMESTAMPDIFF(YEAR, birth_date, CURDATE())
```
para calcular edades directamente desde MySQL.

Luego se aplicaron funciones agregadas:

* AVG
* MIN
* MAX



# Consulta SQL equivalente
```
SELECT

  AVG(TIMESTAMPDIFF(YEAR, birth_date, CURDATE())) AS edad_promedio,

  MIN(TIMESTAMPDIFF(YEAR, birth_date, CURDATE())) AS edad_minima,

  MAX(TIMESTAMPDIFF(YEAR, birth_date, CURDATE())) AS edad_maxima

FROM personas

WHERE birth_date IS NOT NULL;
```
## Manejo de tabla vacía

Se implementó una validación adicional con el fin de evitar errores en tiempo de ejecución cuando no existen personas registradas con fecha de nacimiento en la base de datos. Esta validación permite manejar de forma controlada los casos en los que la información es inexistente o incompleta, garantizando que la API responda correctamente sin generar excepciones y mejorando la estabilidad del sistema.

## Validación implementada
```
if row.promedio is None:
```
## Respuesta controlada 
```
{

  "edad_promedio": 0,

  "edad_minima": 0,

  "edad_maxima": 0

}
```
# Función 3 — Cumpleaños por mes

## Objetivo

Consultar las personas cuyo cumpleaños pertenece a un mes específico, permitiendo filtrar los registros según el mes indicado por el usuario. Esta funcionalidad facilita la obtención de listados organizados de personas que cumplen años en un periodo determinado, mejorando la capacidad de consulta y análisis de datos dentro del sistema.


## Código implementado
```
def cumpleanios_por_mes(db: Session, numero_mes: int):
```
## Lógica implementada

Se utilizó:
```
extract("month", Persona.birth_date)
```
para filtrar registros por mes.

## Consulta SQL equivalente
```
SELECT *

FROM personas

WHERE MONTH(birth_date) = 12;
```
Resultado esperado

Listado de personas que cumplen años en el mes consultado.



# 3. Modificación de Controllers

## Archivo modificado
```
app/controllers/persona_controller.py
```
¿Qué se modificó?

Se agregaron nuevos imports:
```
from typing import Any, List

from fastapi import HTTPException

from ..views.persona import PersonaLabRead

from ..services import persona_analitica_fechas
```

ya que los nuevos endpoints necesitaban:

* listas tipadas
* manejo de errores HTTP
* nuevos schemas
* acceso al nuevo service analítico

#Endpoint 1 — Estadísticas dominios

## Endpoint agregado
```
@router.get("/estadisticas/dominios")
```
Función
```
def estadisticas_dominios(db: Session = Depends(get_db)):
```
## Resultado

Permite consultar estadísticas agrupadas por dominio de correo electrónico, proporcionando un análisis organizado de la distribución de los usuarios según sus proveedores de email. Esta funcionalidad facilita la identificación de patrones en los registros y mejora la capacidad de análisis de la información almacenada en el sistema.

# Endpoint 2 — Estadísticas edad

## Endpoint agregado
```
@router.get("/estadisticas/edad")
```
## Resultado

Permite obtener estadísticas relacionadas con la edad de las personas registradas en la base de datos, incluyendo cálculos como edad promedio, mínima y máxima. Esto facilita el análisis demográfico de los usuarios y aporta información útil para la toma de decisiones dentro del sistema.


# Endpoint 3 — Cumpleaños por mes

## Endpoint agregado
```
@router.get("/cumpleanios/mes/{numero_mes}")
```
## Validaciones implementadas

Se validó que el mes esté entre:
```
1 y 12
```
## Manejo de errores
```
raise HTTPException(

    status_code=400,

    detail="El mes debe ser un entero entre 1 y 12.",

)
```
# Resultado

El endpoint devuelve:

* lista de personas válidas
* error controlado para meses inválidos

# 4. Validaciones realizadas

## Swagger/OpenAPI

Se probaron todos los endpoints desde:
```
http://127.0.0.1:8000/docs
```
# curl

Se realizaron pruebas desde terminal utilizando:
```
curl
```
# Postman

Se creó colección de pruebas con:

* estadísticas dominios
* estadísticas edad
* cumpleaños por mes
* validación de error 400

# DBeaver

Se validaron manualmente las consultas SQL directamente sobre MySQL.


# Control de versiones

Se trabajó utilizando Git y GitHub con commits organizados por funcionalidad.


# Commits realizados
```
feat(views): agregar PersonaLabRead para endpoints analiticos

feat(service): crear servicio persona_analitica_fechas e imports necesarios

feat(service): implementar estadísticas por dominio de correo

feat(controller): agregar endpoint estadisticas dominios

feat(service): implementar estadísticas de edad con TIMESTAMPDIFF

feat(controller): agregar endpoint estadisticas edad

feat(service): implementar filtro cumpleaños por mes

feat(controller): agregar endpoint cumpleaños por mes

test(postman): agregar requests de endpoints analiticos

docs(readme): documentar implementacion analitica y filtros por fecha
```

# Tecnologías utilizadas

* Python 3.11
* FastAPI
* SQLAlchemy
* MySQL
* Pydantic
* Swagger/OpenAPI
* DBeaver
* Postman
* Git
* GitHub
* Visual Studio Code


# Resultado final

Se logró implementar exitosamente un módulo analítico para el sistema CRUD de Personas utilizando:

* consultas SQL avanzadas
* validaciones HTTP
* filtros por fecha
* arquitectura desacoplada
* tipado con Pydantic
* separación por capas
* pruebas funcionales y validación en base de datos