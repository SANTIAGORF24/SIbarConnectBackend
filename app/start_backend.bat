@echo off
REM Script para iniciar el backend SIbarConnect en Windows

echo 🚀 Iniciando SIbarConnect Backend...
echo.

REM Activar el entorno virtual
echo 📦 Activando entorno virtual...
call venv\Scripts\activate.bat

REM Verificar que el .env existe
if not exist .env (
    echo ❌ Error: No se encontró el archivo .env
    echo Por favor, crea el archivo .env con la configuración de la base de datos
    pause
    exit /b 1
)

echo ✅ Entorno virtual activado
echo.

REM Verificar dependencias
echo 🔍 Verificando dependencias...
python -c "import fastapi, uvicorn, sqlalchemy, asyncpg" 2>nul
if errorlevel 1 (
    echo ❌ Error: Faltan dependencias
    echo Ejecuta: pip install -r requirements.txt
    pause
    exit /b 1
)

echo ✅ Dependencias instaladas
echo.

REM Iniciar el servidor
echo 🌟 Iniciando servidor en http://127.0.0.1:8000
echo 📚 Documentación API: http://127.0.0.1:8000/docs
echo.
echo Presiona CTRL+C para detener el servidor
echo.

uvicorn main:app --reload --host 127.0.0.1 --port 8000

pause

