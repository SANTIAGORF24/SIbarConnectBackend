# Archivo Principal - main.py

## Descripción

El archivo `main.py` es el punto de entrada principal de la aplicación FastAPI. Este archivo configura la aplicación, inicializa la base de datos y registra todas las rutas disponibles.

## Código Completo

```python
from fastapi import FastAPI
from core import Settings
from core.database import Base, engine
from models.users.user import User
import asyncio
from routers.user import users
from routers.auth import auth

app = FastAPI(
    title=Settings().app_name
)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")  
def read_root():
    return{
        "app_name": Settings().app_name,
        "app_version": Settings().app_version,
    }

app.include_router(users.router)
app.include_router(auth.router)
```

## Análisis Detallado

### **🚀 Configuración de la Aplicación FastAPI**

```python
app = FastAPI(
    title=Settings().app_name
)
```

**Características**:
- **Título dinámico**: Se obtiene desde variables de entorno
- **Documentación automática**: OpenAPI/Swagger generada automáticamente
- **Configuración mínima**: Setup básico sin configuraciones adicionales

**Configuración expandida recomendada**:
```python
app = FastAPI(
    title=Settings().app_name,
    version=Settings().app_version,
    description="API REST para gestión de usuarios y autenticación",
    docs_url="/docs",
    redoc_url="/redoc"
)
```

### **🔄 Event Handler de Startup**

```python
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
```

**Propósito**: Inicializar la base de datos al arrancar la aplicación

**Proceso**:
1. **Conexión a BD**: Abre conexión asíncrona
2. **Creación de tablas**: Ejecuta DDL para todas las tablas definidas
3. **Importación de modelos**: Requiere que `User` esté importado para incluir la tabla

**⚠️ Consideraciones**:
- **Importación necesaria**: `from models.users.user import User` es crucial
- **Desarrollo vs Producción**: En producción se prefieren migraciones controladas
- **Idempotencia**: `create_all()` solo crea tablas que no existen

### **🏠 Endpoint Root**

```python
@app.get("/")  
def read_root():
    return{
        "app_name": Settings().app_name,
        "app_version": Settings().app_version,
    }
```

**Propósito**: Endpoint de información básica de la aplicación

**Respuesta típica**:
```json
{
    "app_name": "SIbarConnect API",
    "app_version": "1.0.0"
}
```

**Casos de uso**:
- **Health check** básico
- **Información de versión** para cliente
- **Verificación de conectividad**

### **🔗 Registro de Routers**

```python
app.include_router(users.router)
app.include_router(auth.router)
```

**Funcionalidad**: Registra todos los endpoints definidos en los routers

**Estructura resultante**:
```
/                          # Información de la app
/user/create              # Crear usuario
/user/infouser/{id}       # Info por ID
/user/infouser            # Info por email
/user/deleteuser/{id}     # Eliminar por ID
/user/deleteuserforemail  # Eliminar por email
/user/updateput/{id}      # Actualizar usuario
/auth/login               # Autenticación
```

## Flujo de Inicialización

### **1. Importaciones**
```python
from fastapi import FastAPI          # Framework principal
from core import Settings            # Configuración
from core.database import Base, engine  # Base de datos
from models.users.user import User   # Modelo para creación de tabla
import asyncio                       # Programación asíncrona
from routers.user import users       # Endpoints de usuarios
from routers.auth import auth        # Endpoints de autenticación
```

### **2. Creación de la App**
- Instancia FastAPI con configuración básica
- Título obtenido desde variables de entorno

### **3. Event Handlers**
- **Startup**: Inicialización de base de datos
- **Shutdown**: (No implementado) Limpieza de recursos

### **4. Definición de Endpoints**
- Endpoint root para información básica

### **5. Registro de Rutas**
- Inclusión de routers modulares
- Estructura de URLs organizada

## Características de FastAPI

### **Documentación Automática**
Una vez iniciada la aplicación:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

### **Validación Automática**
- Esquemas Pydantic validan automáticamente requests/responses
- Errores 422 para datos inválidos
- Serialización JSON automática

### **Async Support**
- Soporte nativo para programación asíncrona
- Compatible con SQLAlchemy async
- Operaciones no bloqueantes

## Ejecución de la Aplicación

### **Desarrollo Local**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### **Producción**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### **Con Gunicorn**
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## Mejoras Recomendadas

### **1. Configuración Expandida**
```python
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=Settings().app_name,
    version=Settings().app_version,
    description="API REST para SIbarConnect",
    contact={
        "name": "Equipo de Desarrollo",
        "email": "dev@sibarconnect.com"
    },
    license_info={
        "name": "MIT"
    }
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configurar según necesidades
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### **2. Middleware de Logging**
```python
import logging
from fastapi import Request
import time

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    logging.info(f"{request.method} {request.url} - {response.status_code} - {process_time:.4f}s")
    return response
```

### **3. Exception Handlers**
```python
from fastapi import HTTPException
from fastapi.responses import JSONResponse

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "path": str(request.url)
        }
    )

@app.exception_handler(500)
async def internal_server_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "status_code": 500
        }
    )
```

### **4. Health Check Mejorado**
```python
from sqlalchemy import text
from core.database import get_db

@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        # Verificar base de datos
        await db.execute(text("SELECT 1"))
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": Settings().app_version,
            "database": "connected"
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
        )
```

### **5. Event Handlers Mejorados**
```python
@app.on_event("startup")
async def startup_event():
    # Inicializar base de datos
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info(f"🚀 {Settings().app_name} v{Settings().app_version} started")

@app.on_event("shutdown")
async def shutdown_event():
    # Limpiar recursos
    await engine.dispose()
    
    logger = logging.getLogger(__name__)
    logger.info("👋 Application shutdown completed")
```

### **6. Versionado de API**
```python
from fastapi import APIRouter

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(users.router)
v1_router.include_router(auth.router)

app.include_router(v1_router)
```

### **7. Métricas y Monitoreo**
```python
from prometheus_fastapi_instrumentator import Instrumentator

# Métricas Prometheus
Instrumentator().instrument(app).expose(app)

@app.get("/metrics")
async def metrics():
    # Endpoint de métricas personalizado
    return {"requests_total": request_counter}
```

## Estructura de Respuesta Estándar

### **Respuesta Exitosa**
```json
{
    "app_name": "SIbarConnect API",
    "app_version": "1.0.0"
}
```

### **Documentación Automática**
La aplicación genera automáticamente:
- Schema OpenAPI 3.0
- Interfaz Swagger UI interactiva
- Documentación ReDoc
- Validación de tipos automática

## Integración con Docker

El `main.py` se ejecuta dentro del contenedor Docker definido en `Dockerfile`:

```dockerfile
# El contenedor expone la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Variables de Entorno Requeridas

Para el funcionamiento completo, se requieren las siguientes variables:

```env
# Aplicación
APP_NAME=SIbarConnect API
APP_VERSION=1.0.0

# Seguridad
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Base de datos
DB_USER=postgres
BD_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=SibarConnectDev
```

Este archivo `main.py` representa el corazón de la aplicación, orquestando todos los componentes y proporcionando el punto de entrada para todas las funcionalidades del sistema.
