# Directorio Test - Pruebas y Validaciones

## Descripción

El directorio `test/` contiene archivos de prueba y scripts de validación para el proyecto. Actualmente incluye pruebas de conectividad y scripts para verificar el funcionamiento de componentes específicos.

## Estructura

```
test/
├── __pycache__/
└── bd.py               # Script de prueba de conexión a base de datos
```

## Propósito del Directorio Test

El directorio de pruebas proporciona:
- **Validación de conectividad** a servicios externos
- **Scripts de verificación** de configuración
- **Pruebas de integración** básicas
- **Herramientas de debugging** para desarrollo

---

## 📄 `bd.py` - Prueba de Conexión a Base de Datos

### **Propósito**
Verificar la conectividad y configuración de la base de datos PostgreSQL de forma independiente

### **Código Implementado**

```python
from sqlalchemy.ext.asyncio import create_async_engine
import asyncio

DATABASE_URL = "postgresql+asyncpg://postgres:Santirf24123#@localhost:5432/SibarConnectDev"

async def test_connection():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(lambda c: None)
    await engine.dispose()

asyncio.run(test_connection())
```

### **Análisis Detallado**

#### **🔧 Configuración de Conexión**

**URL de Base de Datos**:
```
postgresql+asyncpg://postgres:Santirf24123#@localhost:5432/SibarConnectDev
```

**Componentes**:
- **Protocolo**: `postgresql+asyncpg` (PostgreSQL con driver asíncrono)
- **Usuario**: `postgres` (usuario de base de datos)
- **Contraseña**: `Santirf24123#` (⚠️ **Hardcodeada - riesgo de seguridad**)
- **Host**: `localhost` (servidor local)
- **Puerto**: `5432` (puerto estándar de PostgreSQL)
- **Base de datos**: `SibarConnectDev` (nombre de la BD de desarrollo)

#### **🔄 Proceso de Prueba**

1. **Creación del Engine**:
   ```python
   engine = create_async_engine(DATABASE_URL, echo=True)
   ```
   - Crea motor de conexión asíncrono
   - `echo=True` imprime SQL queries en consola

2. **Prueba de Conexión**:
   ```python
   async with engine.begin() as conn:
       await conn.run_sync(lambda c: None)
   ```
   - Abre transacción de prueba
   - Ejecuta función vacía para validar conectividad
   - Cierra automáticamente la conexión

3. **Limpieza de Recursos**:
   ```python
   await engine.dispose()
   ```
   - Cierra pool de conexiones
   - Libera recursos de red

4. **Ejecución**:
   ```python
   asyncio.run(test_connection())
   ```
   - Ejecuta la función asíncrona desde contexto síncrono

### **Casos de Uso**

#### ✅ **Conexión Exitosa**
```
INFO:sqlalchemy.engine.Engine:BEGIN (implicit)
INFO:sqlalchemy.engine.Engine:COMMIT
```

#### ❌ **Errores Comunes**

**Base de datos no existe**:
```
FATAL: database "SibarConnectDev" does not exist
```

**Credenciales incorrectas**:
```
FATAL: password authentication failed for user "postgres"
```

**Servidor no disponible**:
```
ConnectionRefusedError: [Errno 61] Connection refused
```

**Puerto bloqueado**:
```
OSError: [Errno 60] Operation timed out
```

### **Funcionalidad y Limitaciones**

#### ✅ **Funcionalidades**

1. **Prueba Rápida**: Validación inmediata de conectividad
2. **Logging Detallado**: `echo=True` muestra actividad SQL
3. **Asíncrono**: Usa el mismo stack que la aplicación principal
4. **Independiente**: No depende de otros módulos del proyecto

#### ⚠️ **Limitaciones y Problemas**

1. **Credenciales Hardcodeadas**: 
   - Contraseña visible en código
   - No usa variables de entorno
   - Riesgo de seguridad en repositorios

2. **Configuración Duplicada**:
   - URL diferente a `core/database.py`
   - Mantenimiento duplicado

3. **Funcionalidad Limitada**:
   - Solo prueba conectividad básica
   - No valida permisos o estructura

4. **Sin Manejo de Errores**:
   - Excepciones no capturadas
   - Mensajes de error poco informativos

## Estado Actual y Recomendaciones

### **Estado Actual**
- ✅ Script funcional para prueba básica
- ⚠️ Problemas de seguridad con credenciales
- ⚠️ Duplicación de configuración
- ❌ Falta de pruebas unitarias estructuradas

### **Mejoras Recomendadas**

#### 1. **Uso de Variables de Entorno**
```python
from core import Settings
from core.database import DATABASE_URL

async def test_connection():
    engine = create_async_engine(DATABASE_URL, echo=True)
    # ... resto del código
```

#### 2. **Manejo de Errores Robusto**
```python
import logging

logger = logging.getLogger(__name__)

async def test_connection():
    try:
        engine = create_async_engine(DATABASE_URL, echo=True)
        async with engine.begin() as conn:
            await conn.run_sync(lambda c: None)
        logger.info("✅ Database connection successful")
        return True
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        return False
    finally:
        if 'engine' in locals():
            await engine.dispose()
```

#### 3. **Pruebas de Funcionalidad Extendidas**
```python
async def test_database_functionality():
    """Prueba funcionalidad completa de la base de datos."""
    try:
        engine = create_async_engine(DATABASE_URL, echo=True)
        async with engine.begin() as conn:
            # Probar creación de tabla temporal
            await conn.run_sync(
                lambda c: c.execute(text("CREATE TEMP TABLE test_table (id INT)"))
            )
            
            # Probar inserción
            await conn.run_sync(
                lambda c: c.execute(text("INSERT INTO test_table VALUES (1)"))
            )
            
            # Probar consulta
            result = await conn.run_sync(
                lambda c: c.execute(text("SELECT * FROM test_table")).fetchone()
            )
            
            assert result[0] == 1
            logger.info("✅ Database functionality test passed")
            
    except Exception as e:
        logger.error(f"❌ Database functionality test failed: {e}")
        raise
    finally:
        await engine.dispose()
```

#### 4. **Suite de Tests Estructurada**
```python
import pytest
from sqlalchemy.sql import text

class TestDatabase:
    """Suite de pruebas para base de datos."""
    
    @pytest.mark.asyncio
    async def test_connection(self):
        """Probar conectividad básica."""
        # Implementación
        
    @pytest.mark.asyncio
    async def test_table_creation(self):
        """Probar creación de tablas."""
        # Implementación
        
    @pytest.mark.asyncio
    async def test_crud_operations(self):
        """Probar operaciones CRUD básicas."""
        # Implementación
```

#### 5. **Script de Health Check**
```python
#!/usr/bin/env python3
"""
Health check script para validar estado del sistema.
Uso: python test/health_check.py
"""

import asyncio
import sys
from datetime import datetime

async def main():
    print(f"🔍 Sistema Health Check - {datetime.now()}")
    
    tests = [
        ("Database Connection", test_database_connection),
        ("Environment Variables", test_environment_config),
        ("Dependencies", test_dependencies),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            await test_func()
            print(f"✅ {test_name}: PASS")
            results.append(True)
        except Exception as e:
            print(f"❌ {test_name}: FAIL - {e}")
            results.append(False)
    
    success_rate = sum(results) / len(results) * 100
    print(f"\n📊 Success Rate: {success_rate:.1f}%")
    
    # Exit with error code if any test failed
    sys.exit(0 if all(results) else 1)

if __name__ == "__main__":
    asyncio.run(main())
```

## Integración con Testing Framework

### **Pytest Configuration**
```python
# conftest.py
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

@pytest.fixture
async def db_session():
    """Fixture para sesión de base de datos de prueba."""
    engine = create_async_engine(TEST_DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession)
    
    async with async_session() as session:
        yield session
    
    await engine.dispose()
```

### **Coverage y Reporting**
```bash
# Instalación de herramientas de testing
pip install pytest pytest-asyncio pytest-cov

# Ejecución con coverage
pytest test/ --cov=app --cov-report=html

# Reporte detallado
pytest test/ -v --tb=short
```

## Dirección Futura

### **Tests Faltantes**
1. **Unit Tests**: Para services, utils, y schemas
2. **Integration Tests**: Para endpoints completos
3. **Performance Tests**: Para carga de base de datos
4. **Security Tests**: Para autenticación y autorización

### **Herramientas Recomendadas**
- **pytest**: Framework de testing principal
- **pytest-asyncio**: Soporte para tests asíncronos
- **factory-boy**: Para crear datos de prueba
- **httpx**: Cliente HTTP para testing de APIs
- **pytest-mock**: Para mocking de dependencias

### **Estructura Sugerida**
```
test/
├── conftest.py              # Configuración de pytest
├── unit/
│   ├── test_services.py     # Tests de services
│   ├── test_utils.py        # Tests de utilities
│   └── test_models.py       # Tests de modelos
├── integration/
│   ├── test_auth_flow.py    # Tests de flujo de autenticación
│   └── test_user_crud.py    # Tests de CRUD de usuarios
├── performance/
│   └── test_database.py     # Tests de performance
└── fixtures/
    └── test_data.py         # Datos de prueba
```
