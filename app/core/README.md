# Directorio Core - Configuración Principal

## Descripción

El directorio `core/` contiene los módulos fundamentales para la configuración y funcionamiento del sistema. Aquí se centraliza la configuración de la aplicación, la conexión a la base de datos y aspectos de seguridad.

## Archivos

### 📄 `__init__.py`
- **Propósito**: Convierte el directorio en un paquete Python
- **Contenido**: Archivo de inicialización del módulo core

### 📄 `config.py`
**Función principal**: Gestión centralizada de configuración mediante variables de entorno

**Características:**
- Utiliza `pydantic-settings` para validación tipada de configuración
- Carga variables desde archivo `.env` usando `python-dotenv`
- Define clase `Settings` con todos los parámetros de configuración

**Variables de configuración:**
```python
class Settings(BaseSettings):
    # Información de la aplicación
    app_name: str                      # Nombre de la aplicación
    app_version: str                   # Versión actual
    
    # Configuración JWT
    SECRET_KEY: str                    # Clave secreta para tokens JWT
    ALGORITHM: str                     # Algoritmo de encriptación (HS256)
    ACCESS_TOKEN_EXPIRE_MINUTES: int   # Tiempo de vida del token en minutos
    
    # Configuración de base de datos PostgreSQL
    BD_USER: str                       # Usuario de la base de datos
    DB_PASSWORD: str                   # Contraseña de la base de datos
    DB_HOST: str                       # Host del servidor de BD
    DB_PORT: str                       # Puerto de conexión
    DB_NAME: str                       # Nombre de la base de datos
```

**Patrón de uso:**
```python
from core import Settings
settings = Settings()
print(settings.app_name)
```

### 📄 `database.py`
**Función principal**: Configuración y gestión de la conexión asíncrona a PostgreSQL

**Componentes principales:**

1. **Engine de base de datos asíncrona:**
   ```python
   engine = create_async_engine(DATABASE_URL, echo=True)
   ```
   - Utiliza `asyncpg` como driver PostgreSQL asíncrono
   - `echo=True` imprime las queries SQL en consola para debugging

2. **Construcción de URL de conexión:**
   ```python
   DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
   ```

3. **Session Maker asíncrona:**
   ```python
   async_session = sessionmaker(
       bind=engine,
       class_=AsyncSession,
       expire_on_commit=False
   )
   ```
   - Crea sesiones de trabajo sobre la base de datos
   - `expire_on_commit=False` evita que los objetos ORM se "expiren" al hacer commit

4. **Base declarativa:**
   ```python
   Base = declarative_base()
   ```
   - Clase base para todos los modelos ORM
   - Cada modelo hereda de esta base para crear tablas

5. **Dependency de FastAPI:**
   ```python
   async def get_db():
       async with async_session() as session:
           try:
               yield session
           finally:
               await session.close()
   ```
   - Función generadora para inyección de dependencias
   - Maneja automáticamente el ciclo de vida de las sesiones
   - Garantiza que las conexiones se cierren correctamente

**Patrón de uso en endpoints:**
```python
@router.post("/endpoint")
async def my_endpoint(db: AsyncSession = Depends(get_db)):
    # Usar db para operaciones de base de datos
    pass
```

### 📄 `security.py`
**Estado**: Archivo vacío
**Propósito previsto**: Configuraciones de seguridad adicionales (middleware, CORS, etc.)

## Arquitectura y Patrones

### 1. **Patrón Settings/Configuration**
- Centralización de toda la configuración en una clase
- Validación automática de tipos con Pydantic
- Separación entre configuración y código

### 2. **Patrón Repository/Session**
- Uso de SQLAlchemy como ORM
- Sesiones asíncronas para operaciones no bloqueantes
- Inyección de dependencias para manejo de conexiones

### 3. **Patrón Dependency Injection**
- FastAPI maneja automáticamente las dependencias
- Garantiza limpieza de recursos (conexiones)

## Dependencias Utilizadas

```python
# Configuración
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Base de datos
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
```

## Flujo de Inicialización

1. **Carga de variables de entorno** (`load_dotenv()`)
2. **Creación de instancia Settings** (validación automática)
3. **Construcción de URL de base de datos**
4. **Creación del engine asíncrono**
5. **Configuración del session maker**
6. **Definición de Base declarativa**

## Consideraciones de Seguridad

- Variables sensibles (passwords, keys) se cargan desde entorno
- No hay hardcoding de credenciales en el código
- Conexiones seguras a base de datos
- Manejo adecuado del ciclo de vida de sesiones

## Mejoras Sugeridas

1. **Completar `security.py`** con configuraciones adicionales
2. **Agregar pool de conexiones configurables**
3. **Implementar retry logic para conexiones**
4. **Añadir logging de conexiones**
5. **Configurar timeouts de conexión**
