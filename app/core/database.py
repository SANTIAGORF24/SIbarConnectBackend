from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from core import Settings
from sqlalchemy.ext.asyncio import AsyncSession


DB_USER= Settings().BD_USER
DB_PASSWORD= Settings().DB_PASSWORD
DB_HOST= Settings().DB_HOST
DB_PORT= Settings().DB_PORT
DB_NAME= Settings().DB_NAME

DATABASE_URL=  f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


#engine = create_async_engine se encarga de crear el objeto que gestiona el pool de conexiones y la comuniacio con la bd
#echo= true se encarga de imprimir en consola las queries SQL

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#Session Marker

async_session = sessionmaker(
    bind=engine,  #crea una ventana de trabajo sobre la base de datos
    class_=AsyncSession,
    expire_on_commit=False, # evita que al hacer commmit() los objetos ORM se "expiren"
)

Base = declarative_base() #Esta es la clase base que van a usar mis modelos, cada clase class User(base): crea una tabla

# Dependency para obtener la sesión de la base de datos
async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()