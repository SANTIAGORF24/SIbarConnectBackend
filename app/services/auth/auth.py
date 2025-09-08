from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from schemas.auth import auth as schemas
from models.users import user as models
from utils.security import verifi_password
from utils.token import Crear_acces_token
from utils.fullname import fullnamecreate

async def Login_usuario(user_query: schemas.LoginUserData, db: AsyncSession):

    result = await db.execute(
        select(models.User).where(models.User.email == user_query.email))

    user_db = result.scalar_one_or_none()
    if user_db is None:
        raise HTTPException(status_code=404, detail="usuario no encontrado")
    
    if not verifi_password(user_query.password, user_db.Password_hash):
        raise HTTPException(status_code=401, detail="contraseña incorrecta")

    fullname = fullnamecreate(user_db)

    token_data = {"sub": user_db.email}
    acces_token = Crear_acces_token(token_data)

    return schemas.LoginUserOut (
        fullname=fullname,
        email=user_db.email,
        acces_token= acces_token,
        token_type= "bearer"
    )
