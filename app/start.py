#!/usr/bin/env python3
"""
Script de inicio para FastAPI en Railway
Lee el puerto desde la variable de entorno PORT
"""
import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )

