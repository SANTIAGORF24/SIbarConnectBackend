# SIbarConnect Backend

## Descripción General

Este es el backend de la aplicación SIbarConnect, desarrollado con **FastAPI** y **SQLAlchemy** con soporte asíncrono. El proyecto implementa una API REST para la gestión de usuarios y autenticación con JWT tokens.

## Tecnologías Principales

- **FastAPI**: Framework web moderno y rápido para crear APIs con Python 3.7+
- **SQLAlchemy**: ORM (Object Relational Mapping) con soporte asíncrono
- **PostgreSQL**: Base de datos relacional con driver asyncpg
- **Pydantic**: Validación de datos y serialización
- **JWT**: Autenticación basada en tokens
- **BCrypt**: Hashing seguro de contraseñas

## Estructura del Proyecto

```
app/
├── main.py                 # Punto de entrada de la aplicación
├── Dockerfile             # Configuración de contenedor Docker
├── requirements.txt       # Dependencias del proyecto
├── core/                  # Configuración principal del sistema
├── models/                # Modelos de base de datos (SQLAlchemy)
├── routers/               # Endpoints de la API (rutas)
├── schemas/               # Esquemas de validación (Pydantic)
├── services/              # Lógica de negocio
├── utils/                 # Utilidades y funciones auxiliares
└── test/                  # Archivos de prueba
```

## Características

- **API REST**: Endpoints para gestión de usuarios y autenticación
- **Autenticación JWT**: Sistema de login con tokens seguros
- **Base de datos asíncrona**: Operaciones no bloqueantes con PostgreSQL
- **Validación de datos**: Esquemas Pydantic para entrada y salida de datos
- **Arquitectura modular**: Separación clara de responsabilidades
- **Hashing de contraseñas**: Seguridad con BCrypt
- **Docker**: Containerización para fácil despliegue

## Funcionalidades Implementadas

### Usuarios
- Crear nuevos usuarios
- Consultar información de usuario por ID
- Consultar usuario por email
- Eliminar usuarios (por ID o email)
- Actualizar información de usuarios

### Autenticación
- Login con email y contraseña
- Generación de tokens JWT
- Verificación de credenciales

## Configuración

El proyecto utiliza variables de entorno para la configuración. Estas se definen en el archivo `.env` y incluyen:

- `APP_NAME`: Nombre de la aplicación
- `APP_VERSION`: Versión de la aplicación
- `SECRET_KEY`: Clave secreta para JWT
- `ALGORITHM`: Algoritmo de encriptación
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Tiempo de expiración del token
- Variables de base de datos (USER, PASSWORD, HOST, PORT, NAME)

## Instalación y Ejecución

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Configurar variables de entorno en archivo `.env`

3. Ejecutar la aplicación:
```bash
uvicorn main:app --reload
```

## API Endpoints

### Autenticación
- `POST /auth/login`: Autenticar usuario

### Usuarios
- `POST /user/create`: Crear nuevo usuario
- `GET /user/infouser/{user_id}`: Obtener información por ID
- `POST /user/infouser`: Obtener información por email
- `DELETE /user/deleteuser/{user_id}`: Eliminar por ID
- `DELETE /user/deleteuserforemail`: Eliminar por email
- `PUT /user/updateput/{user_id}`: Actualizar usuario

## Estado del Proyecto

✅ **Implementado:**
- Gestión básica de usuarios
- Autenticación con JWT
- CRUD completo de usuarios
- Validación de datos
- Hashing de contraseñas

🔄 **En desarrollo:**
- Tests unitarios
- Documentación API completa
- Middleware de autenticación
- Roles y permisos
