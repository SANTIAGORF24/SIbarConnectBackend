# Directorio Utils - Utilidades y Funciones Auxiliares

## Descripción

El directorio `utils/` contiene funciones auxiliares y utilidades que proporcionan funcionalidad común reutilizable en toda la aplicación. Estas utilidades encapsulan operaciones específicas como seguridad, generación de tokens y manipulación de datos.

## Estructura

```
utils/
├── __pycache__/
├── fullname.py          # Utilidad para construcción de nombres completos
├── security.py          # Utilidades de seguridad y hashing
└── token.py            # Utilidades para manejo de tokens JWT
```

## Propósito de las Utilidades

Las utilidades proporcionan:
- **Funciones reutilizables** entre diferentes módulos
- **Encapsulación de lógica específica**
- **Abstracción de operaciones complejas**
- **Consistencia** en operaciones similares
- **Mantenibilidad** del código

---

## 📄 `fullname.py` - Construcción de Nombres Completos

### **Propósito**
Generar nombres completos a partir de los campos separados del modelo User

### **Función Principal**

#### 📝 `fullnamecreate(data)`

**Responsabilidad**: Construir un nombre completo concatenando todos los nombres y apellidos disponibles

```python
def fullnamecreate(data):
    fullname = " ".join(filter(None, [
        getattr(data, "first_name_one", None),
        getattr(data, "first_name_two", None),
        getattr(data, "last_name_one", None),
        getattr(data, "last_name_two", None)
    ]))
    
    return fullname
```

**Características**:
- **Manejo de valores nulos**: `filter(None, ...)` elimina campos vacíos
- **Acceso seguro a atributos**: `getattr()` con valor por defecto
- **Flexibilidad**: Funciona con cualquier objeto que tenga estos atributos
- **Espacios correctos**: `" ".join()` une con espacios únicos

**Ejemplos de uso**:
```python
# Usuario con todos los nombres
user = User(
    first_name_one="Juan",
    first_name_two="Carlos", 
    last_name_one="Pérez",
    last_name_two="González"
)
# Resultado: "Juan Carlos Pérez González"

# Usuario sin segundo nombre
user = User(
    first_name_one="María",
    first_name_two=None,
    last_name_one="López",
    last_name_two="Martínez"
)
# Resultado: "María López Martínez"
```

**Casos de uso en el sistema**:
- Respuestas de autenticación (`LoginUserOut.fullname`)
- Información de usuario (`UserInfo.fullname`)
- Mensajes de confirmación de eliminación
- Logs y auditoría

---

## 📄 `security.py` - Utilidades de Seguridad

### **Propósito**
Manejar el hashing y verificación segura de contraseñas usando BCrypt

### **Configuración**

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])
```

**Características de BCrypt**:
- **Salt automático**: Cada hash tiene salt único
- **Costo configurable**: Resistencia a ataques de fuerza bruta
- **Estándar de seguridad**: Algoritmo recomendado para contraseñas

### **Funciones Implementadas**

#### 🔐 `hash_password(password: str) -> str`

**Responsabilidad**: Generar hash seguro de una contraseña en texto plano

```python
def hash_password(password: str) -> str:
    return pwd_context.hash(password)
```

**Proceso**:
1. Recibe contraseña en texto plano
2. Genera salt aleatorio
3. Aplica algoritmo BCrypt
4. Retorna hash seguro

**Ejemplo**:
```python
plain_password = "mi_contraseña_123"
hashed = hash_password(plain_password)
# Resultado: "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
```

#### ✅ `verifi_password(plain_password: str, hased_password: str) -> bool`

**Responsabilidad**: Verificar si una contraseña en texto plano coincide con un hash

```python
def verifi_password(plain_password: str, hased_password: str) -> bool:
    return pwd_context.verify(plain_password, hased_password)
```

**Proceso**:
1. Recibe contraseña en texto plano
2. Recibe hash almacenado
3. Verifica coincidencia usando BCrypt
4. Retorna `True` si coincide, `False` si no

**Uso en autenticación**:
```python
# En el service de login
if not verifi_password(user_query.password, user_db.Password_hash):
    raise HTTPException(status_code=401, detail="contraseña incorrecta")
```

**Ventajas de BCrypt**:
- **Resistente a rainbow tables**: Salt único por contraseña
- **Ajustable computacionalmente**: Factor de costo configurable
- **Estándar probado**: Ampliamente usado y auditado

---

## 📄 `token.py` - Utilidades de Tokens JWT

### **Propósito**
Generar y manejar tokens JWT para autenticación y autorización

### **Configuración**

```python
from datetime import datetime, timedelta
from jose import jwt
from core import Settings

SECRET_KEY = Settings().SECRET_KEY
ALGORITHM = Settings().ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = Settings().ACCESS_TOKEN_EXPIRE_MINUTES
```

**Dependencias de configuración**:
- **SECRET_KEY**: Clave secreta para firmar tokens
- **ALGORITHM**: Algoritmo de firmado (típicamente HS256)
- **ACCESS_TOKEN_EXPIRE_MINUTES**: Tiempo de vida del token

### **Función Principal**

#### 🎫 `Crear_acces_token(data: dict, expires_delta: int = ACCESS_TOKEN_EXPIRE_MINUTES)`

**Responsabilidad**: Generar token JWT con payload personalizado y expiración

```python
def Crear_acces_token(data: dict, expires_delta: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()                           # Copia del payload
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)  # Tiempo de expiración
    to_encode.update({"exp": expire})                 # Añadir claim de expiración
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # Firmar token
    return encoded_jwt
```

**Proceso de generación**:
1. **Copia datos**: Evita modificar el diccionario original
2. **Calcula expiración**: Timestamp UTC futuro
3. **Añade claim 'exp'**: Estándar JWT para expiración
4. **Firma token**: Usando clave secreta y algoritmo
5. **Retorna token**: String codificado listo para uso

**Payload típico**:
```python
token_data = {"sub": "usuario@example.com"}  # 'sub' = subject (usuario)
token = Crear_acces_token(token_data)
```

**Token JWT resultante**:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c3VhcmlvQGV4YW1wbGUuY29tIiwiZXhwIjoxNjkzNDU2Nzg5fQ.signature
```

**Estructura del token**:
- **Header**: `{"alg": "HS256", "typ": "JWT"}`
- **Payload**: `{"sub": "usuario@example.com", "exp": 1693456789}`
- **Signature**: Firmado con SECRET_KEY

**Uso en autenticación**:
```python
# En el service de login
token_data = {"sub": user_db.email}
access_token = Crear_acces_token(token_data)

return LoginUserOut(
    fullname=fullname,
    email=user_db.email,
    acces_token=access_token,
    token_type="bearer"
)
```

## Análisis de las Utilidades

### ✅ **Fortalezas**

1. **Separación de Responsabilidades**: Cada utility tiene propósito específico
2. **Reutilización**: Funciones usadas en múltiples servicios
3. **Seguridad**: Implementación estándar de BCrypt y JWT
4. **Configurabilidad**: Parámetros desde variables de entorno
5. **Simplicidad**: APIs claras y fáciles de usar

### 📊 **Patrones Implementados**

#### **1. Utility/Helper Pattern**
- Funciones estáticas sin estado
- Operaciones puras y predecibles

#### **2. Strategy Pattern (BCrypt)**
- Encapsulación del algoritmo de hashing
- Fácil cambio de implementación

#### **3. Factory Pattern (JWT)**
- Creación de tokens con configuración centralizada

### 🔄 **Flujo de Uso**

```
Service → Utility Function → External Library → Result → Service
```

## Dependencias Externas

### **Passlib**
```python
from passlib.context import CryptContext
```
- Biblioteca de hashing de contraseñas
- Soporte para múltiples algoritmos
- BCrypt como esquema principal

### **Python-JOSE**
```python
from jose import jwt
```
- Implementación JWT para Python
- Soporte para múltiples algoritmos
- Manejo de claims estándar

### **Datetime**
```python
from datetime import datetime, timedelta
```
- Manejo de fechas y tiempos
- Cálculo de expiración de tokens

## Casos de Uso en el Sistema

### **Security Utils**
- **Registro de usuarios**: Hash de contraseña nueva
- **Login**: Verificación de credenciales
- **Cambio de contraseña**: Hash de nueva contraseña

### **Token Utils**
- **Autenticación**: Generación de access token
- **Renovación**: Nuevos tokens para sesiones activas
- **API calls**: Tokens para autorización

### **Fullname Utils**
- **Respuestas API**: Nombres completos en responses
- **Logs**: Identificación legible de usuarios
- **Reportes**: Nombres para documentos

## Mejoras Sugeridas

### 1. **Validaciones de Contraseña**
```python
def validate_password_strength(password: str) -> bool:
    """Validar fortaleza de contraseña."""
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    return True

def hash_password(password: str) -> str:
    if not validate_password_strength(password):
        raise ValueError("Password does not meet strength requirements")
    return pwd_context.hash(password)
```

### 2. **Token Refresh**
```python
def create_refresh_token(data: dict) -> str:
    """Crear token de refresh con mayor duración."""
    expires_delta = timedelta(days=7)  # 7 días para refresh
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> dict:
    """Verificar y decodificar token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except jwt.JWTError:
        raise HTTPException(401, "Invalid token")
```

### 3. **Fullname Mejorado**
```python
def fullnamecreate(data, format_style: str = "full") -> str:
    """Crear nombre completo con diferentes formatos."""
    names = {
        "first_one": getattr(data, "first_name_one", ""),
        "first_two": getattr(data, "first_name_two", ""),
        "last_one": getattr(data, "last_name_one", ""),
        "last_two": getattr(data, "last_name_two", "")
    }
    
    if format_style == "full":
        return " ".join(filter(None, names.values()))
    elif format_style == "formal":
        # "Apellido, Nombre"
        first_names = " ".join(filter(None, [names["first_one"], names["first_two"]]))
        last_names = " ".join(filter(None, [names["last_one"], names["last_two"]]))
        return f"{last_names}, {first_names}"
    elif format_style == "initials":
        # "J.C. Pérez González"
        initials = "".join([n[0] + "." for n in [names["first_one"], names["first_two"]] if n])
        last_names = " ".join(filter(None, [names["last_one"], names["last_two"]]))
        return f"{initials} {last_names}"
```

### 4. **Configuración Avanzada de Seguridad**
```python
from passlib.context import CryptContext

# Configuración más robusta
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12,  # Costo más alto
    bcrypt__ident="2b"  # Versión específica
)

def hash_password_with_pepper(password: str) -> str:
    """Hash con pepper adicional para mayor seguridad."""
    pepper = Settings().PASSWORD_PEPPER
    seasoned_password = password + pepper
    return pwd_context.hash(seasoned_password)
```

### 5. **Logging de Seguridad**
```python
import logging

security_logger = logging.getLogger("security")

def hash_password(password: str) -> str:
    security_logger.info("Password hashing requested")
    return pwd_context.hash(password)

def verifi_password(plain_password: str, hashed_password: str) -> bool:
    result = pwd_context.verify(plain_password, hashed_password)
    if not result:
        security_logger.warning("Password verification failed")
    return result
```

### 6. **Métricas de Tokens**
```python
from functools import wraps

def track_token_creation(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Métricas de creación de tokens
        token = func(*args, **kwargs)
        # Log o envío a sistema de métricas
        return token
    return wrapper

@track_token_creation
def Crear_acces_token(data: dict, expires_delta: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    # Implementación existente
    pass
```
