# Directorio Routers - Endpoints de la API

## Descripción

El directorio `routers/` contiene las definiciones de los endpoints de la API REST. Cada módulo agrupa endpoints relacionados por funcionalidad, siguiendo el patrón de separación por dominio.

## Estructura

```
routers/
├── auth/
│   ├── __pycache__/
│   └── auth.py          # Endpoints de autenticación
└── user/
    ├── __pycache__/
    └── users.py         # Endpoints de gestión de usuarios
```

## Patrón Arquitectónico

Los routers implementan el patrón **Controller** del MVC, donde:
- **Reciben requests HTTP**
- **Validan datos de entrada** (con esquemas Pydantic)
- **Delegan lógica de negocio** a los services
- **Retornan responses estructuradas**

---

## 📁 Auth Module - Autenticación

### 📄 `auth/auth.py`

**Propósito**: Gestiona la autenticación de usuarios mediante JWT tokens

#### **Configuración del Router**
```python
router = APIRouter(
    prefix="/auth",           # Prefijo para todas las rutas
    tags=["auth"]            # Agrupación en documentación OpenAPI
)
```

#### **Endpoints Implementados**

### 🔐 `POST /auth/login`

**Función**: Autenticar usuario y generar token de acceso

**Parámetros**:
- **Body**: `LoginUserData` (email y password)
- **Database**: Inyección de dependencia de sesión DB

**Request Schema**:
```json
{
    "email": "usuario@example.com",
    "password": "contraseña_texto_plano"
}
```

**Response Schema**:
```json
{
    "fullname": "Juan Carlos Pérez González",
    "email": "usuario@example.com",
    "acces_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
}
```

**Flujo de Proceso**:
1. Recibe credenciales del usuario
2. Valida formato con esquema Pydantic
3. Delega autenticación al service `authservices.Login_usuario()`
4. Retorna token JWT si las credenciales son válidas
5. HTTP 200 OK en éxito, 401/404 en error

**Códigos de Estado**:
- `200 OK`: Autenticación exitosa
- `401 Unauthorized`: Contraseña incorrecta
- `404 Not Found`: Usuario no encontrado
- `422 Unprocessable Entity`: Datos inválidos

---

## 📁 User Module - Gestión de Usuarios

### 📄 `user/users.py`

**Propósito**: Proporciona endpoints para CRUD completo de usuarios

#### **Configuración del Router**
```python
router = APIRouter(
    prefix="/user",           # Prefijo para todas las rutas
    tags=["users"]           # Agrupación en documentación OpenAPI
)
```

#### **Endpoints Implementados**

### 👤 `POST /user/create`

**Función**: Crear nuevo usuario en el sistema

**Request Body**: `UserCreate`
```json
{
    "first_name_one": "Juan",
    "first_name_two": "Carlos",
    "last_name_one": "Pérez",
    "last_name_two": "González",
    "email": "juan@example.com",
    "password": "contraseña123"
}
```

**Response**: `UserOut` (HTTP 201)
```json
{
    "id": 1,
    "email": "juan@example.com",
    "is_active": true
}
```

---

### 🔍 `GET /user/infouser/{user_id}`

**Función**: Obtener información de usuario por ID

**Parámetros**:
- **Path**: `user_id` (entero)

**Response**: `UserInfo` (HTTP 200)
```json
{
    "id": 1,
    "email": "juan@example.com",
    "fullname": "Juan Carlos Pérez González"
}
```

---

### 🔍 `POST /user/infouser`

**Función**: Obtener información de usuario por email

**Request Body**: `UserInfoName`
```json
{
    "email": "juan@example.com"
}
```

**Response**: `UserInfo` (HTTP 200)
```json
{
    "id": 1,
    "email": "juan@example.com",
    "fullname": "Juan Carlos Pérez González"
}
```

---

### 🗑️ `DELETE /user/deleteuser/{user_id}`

**Función**: Eliminar usuario por ID

**Parámetros**:
- **Path**: `user_id` (entero)

**Response**: Mensaje de confirmación (HTTP 200)
```json
{
    "message": "El usuario Juan Carlos Pérez González ha sido eliminado"
}
```

---

### 🗑️ `DELETE /user/deleteuserforemail`

**Función**: Eliminar usuario por email

**Request Body**: `DeleteUserForEmail`
```json
{
    "email": "juan@example.com"
}
```

**Response**: Mensaje de confirmación (HTTP 200)

---

### ✏️ `PUT /user/updateput/{user_id}`

**Función**: Actualizar información completa del usuario

**Parámetros**:
- **Path**: `user_id` (entero)
- **Body**: `UpdateUserPut`

**Request Body**:
```json
{
    "first_name_one": "Juan",
    "first_name_two": "Carlos",
    "last_name_one": "Pérez",
    "last_name_two": "González",
    "email": "nuevo_email@example.com"
}
```

**Response**: `UpdateUserPutOut` (HTTP 200)

## Características de los Routers

### ✅ **Fortalezas**

1. **Separación de Responsabilidades**: Cada router maneja un dominio específico
2. **Validación Automática**: Esquemas Pydantic validan entrada y salida
3. **Documentación Automática**: Tags y schemas generan OpenAPI/Swagger
4. **Inyección de Dependencias**: Manejo automático de conexiones DB
5. **Códigos HTTP Apropiados**: Uso correcto de status codes
6. **Async/Await**: Operaciones no bloqueantes

### 📊 **Patrón de Estructura**

Cada endpoint sigue el patrón:
```python
@router.method("/ruta", response_model=Schema, status_code=HTTP_STATUS)
async def nombre_funcion(parametros, db: AsyncSession = Depends(get_db)):
    return await service.metodo_correspondiente(parametros, db)
```

### 🔄 **Flujo de Request/Response**

1. **Request llega al router**
2. **FastAPI valida parámetros** con schemas
3. **Se inyecta sesión de BD** via dependency
4. **Router delega al service** correspondiente
5. **Service ejecuta lógica de negocio**
6. **Response se serializa** con schema de salida
7. **Cliente recibe respuesta JSON**

## Integración con el Sistema

### **Con Schemas** (`schemas/`)
- Validan datos de entrada y salida
- Proporcionan documentación automática
- Garantizan consistencia de tipos

### **Con Services** (`services/`)
- Encapsulan toda la lógica de negocio
- Mantienen routers simples y enfocados
- Permiten reutilización de lógica

### **Con Database** (`core/database.py`)
- Inyección automática de sesiones
- Manejo del ciclo de vida de conexiones
- Transacciones automáticas

## Convenciones Implementadas

### **Nomenclatura de Endpoints**
- **POST**: Crear recursos (`/create`)
- **GET**: Obtener recursos (`/infouser`)
- **PUT**: Actualizar completo (`/updateput`)
- **DELETE**: Eliminar recursos (`/deleteuser`)

### **Códigos de Estado HTTP**
- **200 OK**: Operación exitosa
- **201 Created**: Recurso creado
- **404 Not Found**: Recurso no encontrado
- **400 Bad Request**: Error de validación
- **422 Unprocessable Entity**: Error de esquema

### **Estructura de Respuesta**
- Respuestas consistentes con schemas
- Mensajes de error descriptivos
- Información completa en responses

## Mejoras Sugeridas

### 1. **Autenticación y Autorización**
```python
@router.get("/protected")
async def protected_endpoint(current_user: User = Depends(get_current_user)):
    pass
```

### 2. **Paginación**
```python
@router.get("/users")
async def list_users(skip: int = 0, limit: int = 100):
    pass
```

### 3. **Filtros y Búsqueda**
```python
@router.get("/users/search")
async def search_users(q: str, filters: UserFilters):
    pass
```

### 4. **Versionado de API**
```python
router = APIRouter(prefix="/v1/user")
```

### 5. **Rate Limiting**
```python
from slowapi import Limiter

@router.post("/create")
@limiter.limit("5/minute")
async def create_user():
    pass
```

### 6. **Logging y Monitoreo**
```python
import logging

@router.post("/create")
async def create_user():
    logger.info(f"Creating user: {user.email}")
```

### 7. **Manejo de Errores Centralizado**
```python
@router.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return JSONResponse(status_code=400, content={"error": str(exc)})
```
