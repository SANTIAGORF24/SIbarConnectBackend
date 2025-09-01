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
