# Configuración de Base de Datos

## Pasos para configurar PostgreSQL local

### 1. Verificar que PostgreSQL esté instalado y corriendo

En Windows:
- Busca "Services" en el menú de inicio
- Busca el servicio "postgresql-x64-XX" (donde XX es la versión)
- Asegúrate de que esté "Running" (en ejecución)

### 2. Crear la base de datos

Abre una terminal y ejecuta:

```bash
# Conectar a PostgreSQL (usa tu contraseña de postgres)
psql -U postgres

# Crear la base de datos
CREATE DATABASE sibarconnect;

# Salir de psql
\q
```

O desde la línea de comandos directamente:

```bash
psql -U postgres -c "CREATE DATABASE sibarconnect;"
```

### 3. Verificar la configuración en .env

El archivo `.env` ya está configurado con:
- DB_USER=postgres
- BD_PASSWORD=postgres (cambia esto si tu contraseña es diferente)
- DB_HOST=localhost
- DB_PORT=5432
- DB_NAME=sibarconnect

**Importante:** Si tu contraseña de PostgreSQL es diferente a "postgres", actualiza `BD_PASSWORD` en el archivo `.env`.

### 4. Ejecutar el backend

Una vez que PostgreSQL esté corriendo y la base de datos esté creada:

```bash
# Activar el entorno virtual
source venv/Scripts/activate

# Ejecutar el servidor
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

El servidor estará disponible en: http://127.0.0.1:8000

### 5. Verificar que funciona

Abre tu navegador en: http://127.0.0.1:8000

Deberías ver:
```json
{
  "app_name": "SIbarConnect Backend",
  "app_version": "1.0.0"
}
```

Documentación de la API: http://127.0.0.1:8000/docs

