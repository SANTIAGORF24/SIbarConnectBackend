from sqlalchemy.ext.asyncio import create_async_engine
import asyncio

DATABASE_URL = "postgresql+asyncpg://postgres:Santirf24123#@localhost:5432/SibarConnectDev"

async def test_connection():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(lambda c: None)
    await engine.dispose()

asyncio.run(test_connection())