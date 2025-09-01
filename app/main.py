from fastapi import FastAPI
from core import Settings
from core.database import Base, engine
from models.users.user import User
import asyncio
from routers.user import users

app = FastAPI(
    title=Settings().app_name
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