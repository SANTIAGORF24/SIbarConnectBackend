from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core import Settings
from core.database import Base, engine
from models.users.user import User
from models.menu.menu import Menu
import asyncio
from routers.user import users
from routers.auth import auth
from routers.menu import menu

app = FastAPI(
    title=Settings().app_name
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://v0-app-with-authentication-kappa.vercel.app",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get ("/")  
def read_root():
    return{
        "app_name": Settings().app_name,
        "app_version": Settings().app_version,
    }

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(menu.router)
