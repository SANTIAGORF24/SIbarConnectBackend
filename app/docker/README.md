# Configuración Docker - Dockerfile y Requirements

## Descripción

Esta documentación cubre los archivos de configuración para el despliegue y gestión de dependencias del proyecto: `Dockerfile` para containerización y `requirements.txt` para dependencias de Python.

---

## 📄 `Dockerfile` - Configuración de Contenedor

### **Código Completo**

```dockerfile
# Imagen base de Python
FROM python:3.11-slim

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiar dependencias (aunque esté vacío)
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Mantener el contenedor vivo aunque no tengas código
CMD ["tail", "-f", "/dev/null"]
```

### **Análisis Detallado**

#### **🐍 Imagen Base**
```dockerfile
FROM python:3.11-slim
```

**Características**:
- **Python 3.11**: Versión moderna con mejoras de rendimiento
- **Slim variant**: Imagen reducida sin paquetes innecesarios
- **Debian-based**: Sistema operativo estable y bien soportado
- **Tamaño**: ~45MB vs ~380MB de la imagen completa

**Ventajas de `slim`**:
- Menor superficie de ataque de seguridad
- Descargas más rápidas
- Menor uso de espacio en disco
- Tiempo de build reducido

#### **📁 Directorio de Trabajo**
```dockerfile
WORKDIR /app
```

**Propósito**:
- Establece `/app` como directorio actual dentro del contenedor
- Todos los comandos posteriores se ejecutan desde esta ubicación
- Organización estándar para aplicaciones web

#### **📋 Copia de Dependencias**
```dockerfile
COPY requirements.txt .
```

**Estrategia**:
- Copia solo el archivo de dependencias primero
- Aprovecha la cache de Docker layers
- Si el código cambia pero las dependencias no, se reutiliza la layer de instalación

#### **📦 Instalación de Dependencias**
```dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```

**Flags utilizados**:
- `--no-cache-dir`: No guarda cache de pip (reduce tamaño de imagen)
- `-r requirements.txt`: Instala desde archivo de requirements

#### **⚠️ Comando de Ejecución Problemático**
```dockerfile
CMD ["tail", "-f", "/dev/null"]
```

**Problemas identificados**:
1. **No ejecuta la aplicación**: Solo mantiene el contenedor vivo
2. **Para desarrollo únicamente**: No es apropiado para producción
3. **Requiere intervención manual**: Necesita `docker exec` para ejecutar la app

### **🔧 Dockerfile Mejorado Recomendado**

```dockerfile
# Multi-stage build para optimización
FROM python:3.11-slim as builder

# Instalar dependencias de compilación
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio para dependencias
WORKDIR /wheels

# Copiar requirements y crear wheels
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt

# Imagen final
FROM python:3.11-slim

# Crear usuario no-root para seguridad
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid 1000 --create-home --shell /bin/bash appuser

# Instalar dependencias del sistema si son necesarias
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Configurar directorio de trabajo
WORKDIR /app

# Copiar wheels desde builder stage
COPY --from=builder /wheels /wheels

# Instalar dependencias de Python
RUN pip install --no-cache-dir --no-index --find-links /wheels -r requirements.txt && \
    rm -rf /wheels

# Copiar código de la aplicación
COPY . .

# Cambiar a usuario no-root
USER appuser

# Exponer puerto
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Comando por defecto
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 📄 `requirements.txt` - Dependencias del Proyecto

### **Contenido Actual**

```pip-requirements
pip install python-jose[cryptography]
pip install passlib[bcrypt]
```

### **⚠️ Problemas Identificados**

1. **Formato incorrecto**: No es formato estándar de requirements.txt
2. **Comandos pip**: Contiene comandos en lugar de especificaciones de paquetes
3. **Versiones no especificadas**: Riesgo de incompatibilidades
4. **Dependencias faltantes**: FastAPI, SQLAlchemy, etc. no están listadas

### **📋 Requirements.txt Corregido**

```pip-requirements
# Web Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0

# Database
sqlalchemy==2.0.23
asyncpg==0.29.0
alembic==1.12.1

# Authentication & Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# Data Validation
pydantic==2.5.0
pydantic-settings==2.1.0
email-validator==2.1.0

# Environment Management
python-dotenv==1.0.0

# Development Dependencies (opcional)
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
black==23.11.0
flake8==6.1.0
mypy==1.7.1
```

### **📦 Análisis de Dependencias**

#### **🚀 Framework Web**
- **FastAPI**: Framework principal para la API
- **Uvicorn**: Servidor ASGI para ejecutar FastAPI

#### **🗄️ Base de Datos**
- **SQLAlchemy**: ORM principal
- **asyncpg**: Driver PostgreSQL asíncrono
- **alembic**: Migraciones de base de datos

#### **🔐 Seguridad**
- **python-jose**: Manejo de tokens JWT
- **passlib**: Hashing de contraseñas con BCrypt
- **python-multipart**: Soporte para form data

#### **✅ Validación**
- **Pydantic**: Validación de datos y serialización
- **email-validator**: Validación específica de emails

#### **⚙️ Configuración**
- **python-dotenv**: Carga de variables de entorno

## Configuración de Docker Compose

### **📄 docker-compose.yml Recomendado**

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/sibarconnect
    depends_on:
      - db
    restart: unless-stopped
    
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: sibarconnect
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
```

## Comandos Docker Útiles

### **🔨 Build y Ejecución**

```bash
# Construir imagen
docker build -t sibarconnect-backend .

# Ejecutar contenedor
docker run -p 8000:8000 sibarconnect-backend

# Docker Compose
docker-compose up --build

# Ejecutar en background
docker-compose up -d
```

### **🔍 Debugging**

```bash
# Ejecutar shell en contenedor
docker exec -it container_name /bin/bash

# Ver logs
docker logs container_name

# Inspeccionar contenedor
docker inspect container_name
```

### **🧹 Limpieza**

```bash
# Detener y remover contenedores
docker-compose down

# Remover volúmenes también
docker-compose down -v

# Limpiar imágenes no utilizadas
docker image prune
```

## Optimizaciones de Producción

### **1. Multi-stage Build**
```dockerfile
# Stage 1: Build dependencies
FROM python:3.11-slim as builder
# ... build process

# Stage 2: Runtime
FROM python:3.11-slim
# ... copy built artifacts
```

### **2. Security Hardening**
```dockerfile
# Non-root user
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# Read-only filesystem
CMD ["--read-only"]
```

### **3. Health Checks**
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
```

### **4. Environment Variables**
```dockerfile
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
```

## CI/CD Integration

### **📄 .dockerignore**
```dockerignore
.git
.gitignore
README.md
Dockerfile
.dockerignore
.pytest_cache
.coverage
htmlcov/
*.pyc
__pycache__/
.env
.venv/
```

### **🔄 GitHub Actions**
```yaml
name: Build and Push Docker Image

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker image
        run: docker build -t ${{ secrets.REGISTRY }}/sibarconnect:latest .
        
      - name: Push to registry
        run: docker push ${{ secrets.REGISTRY }}/sibarconnect:latest
```

## Monitoreo y Logging

### **📊 Logging Configuration**
```dockerfile
# Install logging dependencies
RUN pip install structlog

# Configure logging
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=INFO
```

### **📈 Metrics Collection**
```dockerfile
# Install metrics dependencies
RUN pip install prometheus-client

# Expose metrics port
EXPOSE 9090
```

## Troubleshooting

### **❌ Problemas Comunes**

1. **Port already in use**:
   ```bash
   docker-compose down
   # o cambiar puerto en docker-compose.yml
   ```

2. **Permission denied**:
   ```bash
   sudo docker build -t app .
   # o agregar usuario a grupo docker
   ```

3. **Out of space**:
   ```bash
   docker system prune -a
   ```

4. **Database connection failed**:
   - Verificar variables de entorno
   - Confirmar que el servicio de BD esté ejecutándose
   - Revisar configuración de red en Docker

Esta configuración Docker proporciona una base sólida para el desarrollo y despliegue del proyecto, con recomendaciones para optimización y producción.
