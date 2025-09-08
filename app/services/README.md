# Directorio Services - Lógica de Negocio

## Descripción

El directorio `services/` contiene la implementación de la lógica de negocio de la aplicación. Los services actúan como una capa intermedia entre los routers (controladores) y los modelos de datos, encapsulando toda la lógica empresarial y las reglas de negocio.

## Estructura

```
services/
├── auth/
│   ├── __pycache__/
│   └── auth.py          # Lógica de autenticación
└── users/
    ├── __pycache__/
    └── users.py         # Lógica de gestión de usuarios
```

## Patrón Arquitectónico

Los services implementan el patrón **Service Layer**, proporcionando:
- **Encapsulación de lógica de negocio**
- **Abstracción de operaciones de datos**
- **Reutilización de código**
- **Separación de responsabilidades**
- **Transaccionalidad**

---

## 📁 Auth Service - Autenticación

### 📄 `auth/auth.py`

**Propósito**: Gestiona el proceso completo de autenticación de usuarios

#### **Función Principal**

### 🔐 `Login_usuario(user_query, db)`

**Responsabilidades**:
1. **Validación de existencia** del usuario
2. **Verificación de credenciales**
3. **Generación de token JWT**
4. **Construcción de respuesta**

**Parámetros**:
- `user_query`: `LoginUserData` - Credenciales del usuario
- `db`: `AsyncSession` - Sesión de base de datos

**Flujo de Ejecución**:

```python
async def Login_usuario(user_query: schemas.LoginUserData, db: AsyncSession):
    # 1. Buscar usuario por email
    result = await db.execute(
        select(models.User).where(models.User.email == user_query.email))
    user_db = result.scalar_one_or_none()
    
    # 2. Validar existencia
    if user_db is None:
        raise HTTPException(status_code=404, detail="usuario no encontrado")
    
    # 3. Verificar contraseña
    if not verifi_password(user_query.password, user_db.Password_hash):
        raise HTTPException(status_code=401, detail="contraseña incorrecta")
    
    # 4. Generar nombre completo
    fullname = fullnamecreate(user_db)
    
    # 5. Crear token JWT
    token_data = {"sub": user_db.email}
    acces_token = Crear_acces_token(token_data)
    
    # 6. Retornar respuesta estructurada
    return schemas.LoginUserOut(
        fullname=fullname,
        email=user_db.email,
        acces_token=acces_token,
        token_type="bearer"
    )
```

**Manejo de Errores**:
- **404**: Usuario no encontrado
- **401**: Contraseña incorrecta
- **500**: Errores de base de datos

**Dependencias Utilizadas**:
- `utils.security.verifi_password`: Verificación de hash BCrypt
- `utils.token.Crear_acces_token`: Generación de JWT
- `utils.fullname.fullnamecreate`: Construcción de nombre completo

---

## 📁 Users Service - Gestión de Usuarios

### 📄 `users/users.py`

**Propósito**: Implementa todas las operaciones CRUD para la entidad Usuario

#### **Funciones Implementadas**

### 👤 `create_user_in_bd(user, db)`

**Responsabilidad**: Crear nuevo usuario con validaciones de negocio

**Proceso**:
1. **Verificar email único**
2. **Hashear contraseña**
3. **Crear instancia del modelo**
4. **Persistir en base de datos**
5. **Retornar usuario creado**

```python
async def create_user_in_bd(user, db: AsyncSession):
    # Verificar si el email ya existe
    stmt = select(models.User).where(models.User.email == user.email)
    result = await db.execute(stmt)
    db_user = result.scalar_one_or_none()
    
    if db_user:
        raise HTTPException(status_code=400, detail="El correo ya existe")
    
    # Hashear contraseña
    hash_pw = hash_password(user.password)
    
    # Crear nueva instancia
    new_user = models.User(
        first_name_one=user.first_name_one,
        first_name_two=user.first_name_two,
        last_name_one=user.last_name_one,
        last_name_two=user.last_name_two,
        email=user.email,
        Password_hash=hash_pw
    )
    
    # Persistir cambios
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return new_user
```

**Validaciones**:
- **Email único**: Previene duplicados
- **Contraseña segura**: Hash BCrypt automático
- **Datos requeridos**: Validados por esquema Pydantic

### 🔍 `consultar_usuario_por_id(user_id, db)`

**Responsabilidad**: Obtener información de usuario por ID

**Proceso**:
1. **Buscar usuario por ID**
2. **Validar existencia**
3. **Generar nombre completo**
4. **Retornar información estructurada**

```python
async def consultar_usuario_por_id(user_id, db: AsyncSession):
    result = await db.execute(
        select(models.User).where(models.User.id == user_id)
    )
    user_bd = result.scalar_one_or_none()
    
    if user_bd is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    fullname = fullnamecreate(user_bd)
    
    return schemas.UserInfo(
        id=user_bd.id,
        email=user_bd.email,
        fullname=fullname
    )
```

### 📧 `obtener_usuario_por_email(email_user, db)`

**Responsabilidad**: Buscar usuario por email

**Similar a búsqueda por ID pero usando email como criterio**

### 🗑️ `eliminar_usuario_por_id(user_id, db)`

**Responsabilidad**: Eliminar usuario por ID

**Proceso**:
1. **Buscar usuario**
2. **Validar existencia**
3. **Generar nombre para log**
4. **Eliminar de base de datos**
5. **Confirmar eliminación**

```python
async def eliminar_usuario_por_id(user_id, db: AsyncSession):
    result = await db.execute(
        select(models.User).where(models.User.id == user_id)
    )
    user_db = result.scalar_one_or_none()
    
    if user_db is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    fullname = fullnamecreate(user_db)
    
    await db.delete(user_db)
    await db.commit()
    
    return {"message": "El usuario " + fullname + " ha sido eliminado"}
```

### 🗑️ `eliminar_usuario_por_email(email_user, db)`

**Responsabilidad**: Eliminar usuario por email

**Similar a eliminación por ID pero usando email como criterio**

### ✏️ `actualizar_usuario_put(user_id, user_data, db)`

**Responsabilidad**: Actualizar información completa del usuario

**Proceso**:
1. **Buscar usuario existente**
2. **Validar existencia**
3. **Actualizar campos**
4. **Persistir cambios**
5. **Retornar datos actualizados**

```python
async def actualizar_usuario_put(user_id: int, user_data: schemas.UpdateUserPut, db: AsyncSession):
    result = await db.execute(
        select(models.User).where(models.User.id == user_id)
    )
    user_db = result.scalar_one_or_none()
    
    if user_db is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Actualizar campos
    user_db.first_name_one = user_data.first_name_one
    user_db.first_name_two = user_data.first_name_two
    user_db.last_name_one = user_data.last_name_one
    user_db.last_name_two = user_data.last_name_two
    user_db.email = user_data.email
    
    await db.commit()
    await db.refresh(user_db)
    
    return schemas.UpdateUserPutOut(
        first_name_one=user_db.first_name_one,
        first_name_two=user_db.first_name_two,
        last_name_one=user_db.last_name_one,
        last_name_two=user_db.last_name_two,
        email=user_db.email
    )
```

## Características de los Services

### ✅ **Fortalezas**

1. **Encapsulación Completa**: Toda la lógica de negocio centralizada
2. **Validaciones de Negocio**: Reglas empresariales aplicadas consistentemente
3. **Manejo de Errores**: HTTPExceptions apropiadas para cada caso
4. **Transaccionalidad**: Operaciones atómicas con commit/rollback
5. **Reutilización**: Funciones reutilizables entre endpoints
6. **Asincronía**: Operaciones no bloqueantes

### 📊 **Patrones Implementados**

#### **1. Repository Pattern**
- Abstracción de acceso a datos
- Operaciones CRUD encapsuladas

#### **2. Business Logic Layer**
- Separación clara entre presentación y datos
- Reglas de negocio centralizadas

#### **3. Error Handling Pattern**
- Manejo consistente de excepciones
- Códigos HTTP apropiados

### 🔄 **Flujo de Operación Típico**

```
Router → Service → Validation → Database → Model → Response → Router
```

1. **Router recibe request**
2. **Service procesa lógica de negocio**
3. **Validaciones específicas de dominio**
4. **Operaciones de base de datos**
5. **Transformación de datos**
6. **Retorno de respuesta estructurada**

## Validaciones de Negocio

### **Usuarios**
- **Email único**: Previene duplicación de cuentas
- **Existencia**: Validación antes de operaciones
- **Integridad de datos**: Campos requeridos verificados

### **Autenticación**
- **Usuario existente**: Verificación previa al login
- **Credenciales válidas**: Hash de contraseña verificado
- **Token válido**: JWT con payload estructurado

## Dependencias y Utilidades

### **Security Utils**
```python
from utils.security import hash_password, verifi_password
```
- Hashing y verificación de contraseñas

### **Token Utils**
```python
from utils.token import Crear_acces_token
```
- Generación de tokens JWT

### **Fullname Utils**
```python
from utils.fullname import fullnamecreate
```
- Construcción de nombres completos

## Manejo de Transacciones

### **Patrón de Transacción**
```python
# Operación de modificación
db.add(new_user)           # Añadir a sesión
await db.commit()          # Confirmar cambios
await db.refresh(new_user) # Actualizar objeto

# Operación de eliminación
await db.delete(user_db)   # Marcar para eliminación
await db.commit()          # Confirmar eliminación
```

### **Rollback Automático**
- FastAPI/SQLAlchemy manejan rollback en caso de error
- Las sesiones se cierran automáticamente

## Mejoras Sugeridas

### 1. **Logging Detallado**
```python
import logging

logger = logging.getLogger(__name__)

async def create_user_in_bd(user, db: AsyncSession):
    logger.info(f"Creating user with email: {user.email}")
    # ... lógica existente
    logger.info(f"User created with ID: {new_user.id}")
```

### 2. **Validaciones Avanzadas**
```python
async def create_user_in_bd(user, db: AsyncSession):
    # Validar formato de email más estricto
    if not is_valid_business_email(user.email):
        raise HTTPException(400, "Email domain not allowed")
```

### 3. **Paginación de Consultas**
```python
async def list_users(skip: int, limit: int, db: AsyncSession):
    result = await db.execute(
        select(models.User).offset(skip).limit(limit)
    )
    return result.scalars().all()
```

### 4. **Soft Delete**
```python
async def soft_delete_user(user_id: int, db: AsyncSession):
    user_db.is_active = False
    user_db.deleted_at = datetime.utcnow()
    await db.commit()
```

### 5. **Cache de Consultas**
```python
from functools import lru_cache

@lru_cache(maxsize=100)
async def get_user_cached(user_id: int):
    # Implementar cache para consultas frecuentes
    pass
```

### 6. **Eventos de Auditoría**
```python
async def create_user_in_bd(user, db: AsyncSession):
    new_user = models.User(...)
    db.add(new_user)
    await db.commit()
    
    # Evento de auditoría
    await audit_service.log_user_creation(new_user.id)
```

### 7. **Validación de Permisos**
```python
async def delete_user(user_id: int, current_user: User, db: AsyncSession):
    if not current_user.is_super_admin:
        raise HTTPException(403, "Insufficient permissions")
```

### 8. **Búsqueda Avanzada**
```python
async def search_users(
    query: str, 
    filters: UserFilters, 
    db: AsyncSession
):
    stmt = select(models.User)
    
    if query:
        stmt = stmt.where(
            models.User.first_name_one.ilike(f"%{query}%")
        )
    
    if filters.is_active is not None:
        stmt = stmt.where(models.User.is_active == filters.is_active)
    
    result = await db.execute(stmt)
    return result.scalars().all()
```
