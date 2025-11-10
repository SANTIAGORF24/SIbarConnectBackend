# Imagen base de Python
FROM python:3.12-slim

# Establecer variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema si son necesarias
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt primero (para aprovechar cache de Docker)
COPY app/requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar todo el código de la aplicación desde app/
COPY app/ .

# Exponer el puerto (Railway lo asignará dinámicamente, pero necesitamos un puerto por defecto)
EXPOSE 8000

# Comando para ejecutar la aplicación
# Railway proporciona la variable de entorno PORT automáticamente
CMD sh -c "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"

