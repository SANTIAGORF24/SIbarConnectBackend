# Directorio Models - Modelos de Base de Datos

## Descripción

El directorio `models/` contiene las definiciones de los modelos de datos usando SQLAlchemy ORM. Estos modelos representan las tablas de la base de datos y definen la estructura, relaciones y comportamiento de los datos.

## Estructura

```
models/
└── users/
    ├── __pycache__/
    └── user.py          # Modelo de usuario
```

## Archivos

### 📁 `users/` - Módulo de Usuarios

#### 📄 `user.py`
**Función principal**: Define el modelo de datos para la entidad Usuario

**Estructura de la clase User:**

```python
class User(Base):
    __tablename__ = "users"
    
    # Campos de la tabla
    id = Column(Integer, primary_key=True, index=True)
    is_super_admin = Column(Boolean, nullable=False, default=False)
    first_name_one = Column(String(20), nullable=False)
    first_name_two = Column(String(20), nullable=True)
    last_name_one = Column(String(20), nullable=False)
    last_name_two = Column(String(20), nullable=False)
    email = Column(String(50), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    Password_hash = Column(String(255), nullable=False)
```

## Análisis Detallado del Modelo User

### 🔑 **Campos de Identificación**

**`id`** - *Clave Primaria*
- **Tipo**: `Integer`
- **Restricciones**: `primary_key=True, index=True`
- **Propósito**: Identificador único autoincrementable
- **Índice**: Automático para optimización de consultas

**`email`** - *Identificador de Usuario*
- **Tipo**: `String(50)`
- **Restricciones**: `nullable=False`
- **Propósito**: Email único del usuario para login
- **Consideración**: Debería tener constraint `unique=True`

### 👤 **Campos de Información Personal**

**`first_name_one`** - *Primer Nombre*
- **Tipo**: `String(20)`
- **Restricciones**: `nullable=False`
- **Propósito**: Primer nombre obligatorio del usuario

**`first_name_two`** - *Segundo Nombre*
- **Tipo**: `String(20)`
- **Restricciones**: `nullable=True`
- **Propósito**: Segundo nombre opcional del usuario

**`last_name_one`** - *Primer Apellido*
- **Tipo**: `String(20)`
- **Restricciones**: `nullable=False`
- **Propósito**: Primer apellido obligatorio

**`last_name_two`** - *Segundo Apellido*
- **Tipo**: `String(20)`
- **Restricciones**: `nullable=False`
- **Propósito**: Segundo apellido obligatorio

### 🔐 **Campos de Seguridad y Estado**

**`is_super_admin`** - *Rol de Administrador*
- **Tipo**: `Boolean`
- **Restricciones**: `nullable=False, default=False`
- **Propósito**: Indica si el usuario tiene privilegios de super administrador

**`is_active`** - *Estado del Usuario*
- **Tipo**: `Boolean`
- **Restricciones**: `nullable=False, default=True`
- **Propósito**: Control de estado activo/inactivo del usuario

**`Password_hash`** - *Contraseña Encriptada*
- **Tipo**: `String(255)`
- **Restricciones**: `nullable=False`
- **Propósito**: Almacena la contraseña hasheada con BCrypt
- **Seguridad**: Nunca almacena contraseñas en texto plano

## Características del Modelo

### ✅ **Fortalezas**

1. **Estructura Clara**: Separación lógica de nombres y apellidos
2. **Seguridad**: Almacenamiento seguro de contraseñas
3. **Flexibilidad**: Campos opcionales para segundo nombre
4. **Control de Estado**: Flags para administración y activación
5. **Herencia Correcta**: Extiende de `Base` para integración con SQLAlchemy

### ⚠️ **Áreas de Mejora**

1. **Constraint de Unicidad**: El email debería ser único
2. **Validaciones**: Falta validación de formato de email a nivel de BD
3. **Índices**: El email debería tener índice para búsquedas rápidas
4. **Timestamps**: Faltan campos de `created_at` y `updated_at`
5. **Relaciones**: No hay relaciones definidas con otras entidades

## Patrones Implementados

### 1. **Active Record Pattern**
- El modelo encapsula tanto datos como comportamiento
- Hereda funcionalidad ORM de SQLAlchemy

### 2. **Data Transfer Object (DTO)**
- Separación clara entre modelo de datos y esquemas de API
- El modelo representa la estructura de BD, no la API

### 3. **Domain Driven Design**
- Organización por dominio (users/)
- Separación clara de responsabilidades

## Uso en el Sistema

### **Creación de Usuario**
```python
new_user = User(
    first_name_one="Juan",
    first_name_two="Carlos",
    last_name_one="Pérez",
    last_name_two="González",
    email="juan@example.com",
    Password_hash=hashed_password
)
```

### **Consultas Comunes**
```python
# Por ID
user = await session.get(User, user_id)

# Por email
stmt = select(User).where(User.email == email)
result = await session.execute(stmt)
user = result.scalar_one_or_none()

# Usuarios activos
stmt = select(User).where(User.is_active == True)
active_users = await session.execute(stmt)
```

## Mapeo a Base de Datos

**Tabla resultante en PostgreSQL:**

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    is_super_admin BOOLEAN NOT NULL DEFAULT FALSE,
    first_name_one VARCHAR(20) NOT NULL,
    first_name_two VARCHAR(20),
    last_name_one VARCHAR(20) NOT NULL,
    last_name_two VARCHAR(20) NOT NULL,
    email VARCHAR(50) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    password_hash VARCHAR(255) NOT NULL
);

-- Índices recomendados
CREATE INDEX idx_users_email ON users(email);
CREATE UNIQUE INDEX unique_users_email ON users(email);
```

## Dependencias

```python
from sqlalchemy import Column, Integer, String, Boolean
from core.database import Base
```

## Integración con el Sistema

### **En Services**
- Los services usan este modelo para operaciones CRUD
- Conversión entre esquemas Pydantic y modelo SQLAlchemy

### **En Schemas**
- Los esquemas Pydantic validan datos antes de crear instancias del modelo
- Serialización del modelo para respuestas API

### **En Routers**
- Los endpoints reciben esquemas y los convierten a modelos
- Retornan esquemas basados en el modelo

## Recomendaciones de Mejora

1. **Agregar constraints de unicidad**:
   ```python
   email = Column(String(50), nullable=False, unique=True, index=True)
   ```

2. **Añadir timestamps**:
   ```python
   created_at = Column(DateTime, default=datetime.utcnow)
   updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
   ```

3. **Implementar relaciones**:
   ```python
   # Ejemplo para futuras entidades
   profile = relationship("UserProfile", back_populates="user")
   ```

4. **Validaciones adicionales**:
   ```python
   @validates('email')
   def validate_email(self, key, email):
       # Validación de formato
       return email
   ```

5. **Métodos de conveniencia**:
   ```python
   @property
   def full_name(self):
       return f"{self.first_name_one} {self.last_name_one}"
   ```
