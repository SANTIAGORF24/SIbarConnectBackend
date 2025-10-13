# 🔐 Autenticación JWT - Guía de Uso

## Rutas Públicas (Sin autenticación)
- `GET /` - Información de la aplicación
- `POST /auth/login` - Iniciar sesión

## Rutas Protegidas (Requieren Bearer Token)
Todas las demás rutas requieren autenticación:
- **Todas las rutas de usuarios** (`/user/*`)
- **Todas las rutas de menú** (`/menu/*`)

## 🚀 Cómo usar la autenticación

### 1. Obtener el token
```bash
POST /auth/login
Content-Type: application/json

{
    "email": "usuario@ejemplo.com",
    "password": "tu_password"
}
```

**Respuesta:**
```json
{
    "fullname": "Nombre Usuario",
    "email": "usuario@ejemplo.com",
    "acces_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "bearer"
}
```

### 2. Usar el token en las rutas protegidas
Incluir en el header `Authorization`:

```bash
GET /menu/all
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### 3. Ejemplo con curl
```bash
# 1. Login
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@ejemplo.com",
    "password": "password123"
  }'

# 2. Usar el token obtenido
curl -X GET "http://localhost:8000/menu/all" \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

### 4. Ejemplo con JavaScript/Fetch
```javascript
// 1. Login
const loginResponse = await fetch('/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'usuario@ejemplo.com',
    password: 'password123'
  })
});

const loginData = await loginResponse.json();
const token = loginData.acces_token;

// 2. Usar el token
const menusResponse = await fetch('/menu/all', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
```

## 🛡️ Manejo de Errores

### Token inválido o expirado (401)
```json
{
    "detail": "Token inválido o expirado",
    "headers": {"WWW-Authenticate": "Bearer"}
}
```

### Token faltante (422)
```json
{
    "detail": [
        {
            "loc": ["header", "authorization"],
            "msg": "field required",
            "type": "value_error.missing"
        }
    ]
}
```

### Usuario no encontrado (401)
```json
{
    "detail": "Usuario no encontrado"
}
```

## ⚙️ Configuración
Los tokens se configuran en el archivo `.env`:
- `SECRET_KEY`: Clave secreta para firmar tokens
- `ALGORITHM`: Algoritmo de encriptación (HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Tiempo de expiración en minutos
