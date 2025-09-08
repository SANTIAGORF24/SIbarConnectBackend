# Directorio Schemas - Validación y Serialización de Datos

## Descripción

El directorio `schemas/` contiene las definiciones de esquemas Pydantic que se utilizan para la validación de datos de entrada y serialización de datos de salida en la API. Estos esquemas actúan como contratos de datos entre el cliente y el servidor.

## Estructura

```
schemas/
├── auth/
│   ├── __pycache__/
│   └── auth.py          # Esquemas de autenticación
└── user/
    ├── __pycache__/
    └── user.py          # Esquemas de usuario
```

## Propósito de los Schemas

Los esquemas Pydantic proporcionan:
- **Validación automática** de tipos de datos
- **Serialización/Deserialización** JSON ↔ Python
- **Documentación automática** OpenAPI/Swagger
- **Transformación de datos** entre capas
- **Validación de reglas de negocio**

---

## 📁 Auth Schemas - Autenticación

### 📄 `auth/auth.py`

**Propósito**: Define los contratos de datos para el proceso de autenticación

#### **Esquemas Implementados**

### 🔐 `LoginUserData` - *Datos de Login*

**Uso**: Validar credenciales de entrada en el endpoint de login

```python
class LoginUserData(BaseModel):
    email: EmailStr      # Email con validación automática de formato
    password: str        # Contraseña en texto plano (se hashea en el service)
```

**Características**:
- **EmailStr**: Validación automática de formato de email
- **password**: String simple, se procesa en la capa de service
- **Propósito**: Request body para `POST /auth/login`

**Ejemplo de uso**:
```json
{
    "email": "usuario@example.com",
    "password": "mi_contraseña_123"
}
```

### 🎫 `LoginUserOut` - *Respuesta de Autenticación*

**Uso**: Estructura de respuesta tras autenticación exitosa

```python
class LoginUserOut(BaseModel):
    fullname: str        # Nombre completo del usuario
    email: EmailStr      # Email del usuario autenticado
    acces_token: str     # Token JWT generado
    token_type: str      # Tipo de token (típicamente "bearer")
```

**Características**:
- **fullname**: Nombre completo construido por el service
- **access_token**: Token JWT para autorización
- **token_type**: Estándar "bearer" para Authorization header
- **Propósito**: Response body para `POST /auth/login`

**Ejemplo de respuesta**:
```json
{
    "fullname": "Juan Carlos Pérez González",
    "email": "usuario@example.com",
    "acces_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
}
```

---

## 📁 User Schemas - Gestión de Usuarios

### 📄 `user/user.py`

**Propósito**: Define todos los contratos de datos para operaciones CRUD de usuarios

#### **Esquemas de Entrada (Input)**

### 👤 `UserCreate` - *Creación de Usuario*

**Uso**: Validar datos para crear nuevo usuario

```python
class UserCreate(BaseModel):
    first_name_one: str                    # Primer nombre (obligatorio)
    first_name_two: Optional[str] = None   # Segundo nombre (opcional)
    last_name_one: str                     # Primer apellido (obligatorio)
    last_name_two: str                     # Segundo apellido (obligatorio)
    email: EmailStr                        # Email único del usuario
    password: str                          # Contraseña en texto plano
```

**Características**:
- **Campos obligatorios**: first_name_one, last_name_one, last_name_two, email, password
- **Campo opcional**: first_name_two
- **Validación de email**: Automática con EmailStr
- **Propósito**: Request body para `POST /user/create`

### 🔍 `UserInfoName` - *Búsqueda por Email*

**Uso**: Obtener información de usuario por email

```python
class UserInfoName(BaseModel):
    email: EmailStr      # Email del usuario a buscar
```

### 🗑️ `DeleteUserForEmail` - *Eliminación por Email*

**Uso**: Eliminar usuario especificando email

```python
class DeleteUserForEmail(BaseModel):
    email: EmailStr      # Email del usuario a eliminar
```

### ✏️ `UpdateUserPut` - *Actualización Completa*

**Uso**: Actualizar información de usuario (PUT)

```python
class UpdateUserPut(BaseModel):
    first_name_one: str                    # Primer nombre actualizado
    first_name_two: Optional[str] = None   # Segundo nombre actualizado
    last_name_one: str                     # Primer apellido actualizado
    last_name_two: str                     # Segundo apellido actualizado
    email: EmailStr                        # Email actualizado
```

**Nota**: No incluye password para evitar cambios accidentales

#### **Esquemas de Salida (Output)**

### 📤 `UserOut` - *Respuesta de Creación*

**Uso**: Respuesta tras crear usuario exitosamente

```python
class UserOut(BaseModel):
    id: int              # ID del usuario creado
    email: EmailStr      # Email del usuario
    is_active: bool      # Estado activo del usuario

    class Config:
        orm_mode = True  # Permite serialización desde objetos SQLAlchemy
```

**Características**:
- **orm_mode**: Permite conversión directa desde modelos SQLAlchemy
- **Campos mínimos**: Solo información esencial tras creación
- **Seguridad**: No expone información sensible

### 📋 `UserInfo` - *Información Detallada*

**Uso**: Respuesta con información completa del usuario

```python
class UserInfo(BaseModel):
    id: int              # ID único del usuario
    email: EmailStr      # Email del usuario
    fullname: str        # Nombre completo construido
```

**Características**:
- **fullname**: Campo calculado por el service
- **Información segura**: No expone datos sensibles
- **Uso múltiple**: Respuesta para varios endpoints

### 📝 `UpdateUserPutOut` - *Respuesta de Actualización*

**Uso**: Confirmar datos actualizados tras PUT

```python
class UpdateUserPutOut(BaseModel):
    first_name_one: str                    # Primer nombre actualizado
    first_name_two: Optional[str] = None   # Segundo nombre actualizado
    last_name_one: str                     # Primer apellido actualizado
    last_name_two: str                     # Segundo apellido actualizado
    email: EmailStr                        # Email actualizado
```

## Análisis de Diseño

### ✅ **Fortalezas del Diseño**

1. **Separación Clara**: Esquemas específicos para cada operación
2. **Validación Automática**: EmailStr valida formato de emails
3. **Campos Opcionales**: Manejo correcto con Optional[str]
4. **Seguridad**: No exposición de contraseñas en responses
5. **ORM Integration**: Config orm_mode para SQLAlchemy
6. **Reutilización**: Esquemas base reutilizables

### 📊 **Patrones Implementados**

#### **1. Input/Output Separation**
- Esquemas diferentes para entrada y salida
- Control granular de qué datos se exponen

#### **2. Data Transfer Object (DTO)**
- Esquemas actúan como DTOs entre capas
- Validación en la frontera de la aplicación

#### **3. Command/Query Responsibility Segregation (CQRS)**
- Esquemas de comando (Create, Update, Delete)
- Esquemas de consulta (UserInfo, UserOut)

### 🔄 **Flujo de Validación**

```
Client Request → Pydantic Schema → Validation → Router → Service → Model
Client Response ← Pydantic Schema ← Serialization ← Router ← Service ← Model
```

## Convenciones y Estándares

### **Nomenclatura**
- **Input schemas**: `EntityAction` (ej: UserCreate, LoginUserData)
- **Output schemas**: `EntityOut` o `EntityInfo` (ej: UserOut, UserInfo)
- **Search schemas**: `EntitySearchTerm` (ej: UserInfoName)

### **Configuración Estándar**
```python
class Config:
    orm_mode = True          # Para modelos SQLAlchemy
    use_enum_values = True   # Para enums
    validate_assignment = True # Validar en asignación
```

### **Tipos Comunes**
- **EmailStr**: Para emails válidos
- **Optional[T]**: Para campos opcionales
- **BaseModel**: Clase base de Pydantic

## Integración con el Sistema

### **Con Routers**
```python
@router.post("/create", response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    return await service.create_user(user, db)
```

### **Con Services**
```python
async def create_user(user: schemas.UserCreate, db: AsyncSession):
    # user es un objeto Pydantic validado
    # Conversión a modelo SQLAlchemy
    db_user = models.User(**user.dict())
```

### **Con Models**
```python
# Serialización automática desde modelo
user_response = schemas.UserOut.from_orm(db_user)
```

## Validaciones Automáticas

### **EmailStr**
- Formato válido de email
- Normalización automática
- Error 422 si formato inválido

### **Tipos Obligatorios**
- ValidationError si falta campo requerido
- Error 422 con detalles específicos

### **Longitud de Strings**
- Pydantic valida automáticamente
- Consistente con restricciones de BD

## Mejoras Sugeridas

### 1. **Validaciones Personalizadas**
```python
from pydantic import validator

class UserCreate(BaseModel):
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v
```

### 2. **Campos Calculados**
```python
from pydantic import Field

class UserInfo(BaseModel):
    fullname: str = Field(description="Full name of the user")
```

### 3. **Respuestas Paginadas**
```python
class UserListResponse(BaseModel):
    users: List[UserInfo]
    total: int
    page: int
    per_page: int
```

### 4. **Esquemas Base**
```python
class BaseUser(BaseModel):
    first_name_one: str
    last_name_one: str
    email: EmailStr

class UserCreate(BaseUser):
    password: str

class UserUpdate(BaseUser):
    pass
```

### 5. **Enums para Estados**
```python
from enum import Enum

class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
```

### 6. **Documentación Mejorada**
```python
class UserCreate(BaseModel):
    """Schema for creating a new user account."""
    
    email: EmailStr = Field(description="Valid email address for the user")
    password: str = Field(min_length=8, description="Password with minimum 8 characters")
```
