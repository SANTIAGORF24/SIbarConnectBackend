#!/bin/bash

# Script para iniciar el backend SIbarConnect

echo "🚀 Iniciando SIbarConnect Backend..."
echo ""

# Activar el entorno virtual
echo "📦 Activando entorno virtual..."
source venv/Scripts/activate

# Verificar que el .env existe
if [ ! -f .env ]; then
    echo "❌ Error: No se encontró el archivo .env"
    echo "Por favor, crea el archivo .env con la configuración de la base de datos"
    exit 1
fi

echo "✅ Entorno virtual activado"
echo ""

# Verificar dependencias
echo "🔍 Verificando dependencias..."
python -c "import fastapi, uvicorn, sqlalchemy, asyncpg" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Error: Faltan dependencias"
    echo "Ejecuta: pip install -r requirements.txt"
    exit 1
fi

echo "✅ Dependencias instaladas"
echo ""

# Iniciar el servidor
echo "🌟 Iniciando servidor en http://127.0.0.1:8000"
echo "📚 Documentación API: http://127.0.0.1:8000/docs"
echo ""
echo "Presiona CTRL+C para detener el servidor"
echo ""

uvicorn main:app --reload --host 127.0.0.1 --port 8000

