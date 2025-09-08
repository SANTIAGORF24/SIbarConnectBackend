from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from models.users import user as models
from schemas.user import user as schemas
from utils.security import hash_password    
from utils.fullname import fullnamecreate


async def create_user_in_bd(user, db: AsyncSession):

    stmt = select(models.User).where(models.User.email == user.email)
    result = await db.execute(stmt)
    db_user= result.scalar_one_or_none()
    if db_user:
        raise HTTPException(status_code=400, detail="El correo ya existe")
    
    hash_pw = hash_password(user.password)
    new_user = models.User(
        first_name_one=user.first_name_one,
        first_name_two=user.first_name_two,
        last_name_one=user.last_name_one,
        last_name_two=user.last_name_two,
        email=user.email,
        Password_hash=hash_pw
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def consultar_usuario_por_id(user_id, db: AsyncSession):
    result = await db.execute(
        select(models.User).where(models.User.id == user_id)

    )
    user_bd = result.scalar_one_or_none()

    if user_bd is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    

    fullname = fullnamecreate(user_bd)

    #devolvemos el esquema
    return schemas.UserInfo(
        id = user_bd.id,
        email = user_bd.email,
        fullname = fullname
    )


async def obtener_usuario_por_email(email_user: schemas.UserInfoName, db: AsyncSession):
    result = await db.execute(
        select(models.User).where(models.User.email == email_user.email)
    )

    user_db = result.scalar_one_or_none()

    if user_db is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    fullname = fullnamecreate(user_db)

    return schemas.UserInfo(
        id=user_db.id,
        email=user_db.email,
        fullname=fullname
    )
    

async def eliminar_usuario_por_id(user_id, db: AsyncSession):
    result = await db.execute(
        select(models.User).where(models.User.id == user_id)
    )
    user_db = result.scalar_one_or_none()
    
    if user_db is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    fullname = fullnamecreate(user_db)

    await db.delete(user_db)
    await db.commit()

    return {"message" : "El usuario " + fullname + "ha sido eliminado"}


async def eliminar_usuario_por_email(email_user: schemas.DeleteUserForEmail, db: AsyncSession):
    result = await db.execute(
        select(models.User).where(models.User.email == email_user.email)
    )

    user_db = result.scalar_one_or_none()

    if user_db is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")


    fullname = fullnamecreate(user_db)

    await db.delete(user_db)
    await db.commit()

    return{"message": "El usuario "+ fullname + " ha sido eliminado"}

async def actualizar_usuario_put(user_id: int, user_data: schemas.UpdateUserPut, db: AsyncSession):
    result= await db.execute(
        select(models.User).where(models.User.id == user_id)
    )

    user_db = result.scalar_one_or_none()

    if user_db is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    user_db.first_name_one = user_data.first_name_one
    user_db.first_name_two = user_data.first_name_two
    user_db.last_name_one = user_data.last_name_one
    user_db.last_name_two = user_data.last_name_two
    user_db.email = user_data.email

    await db.commit()
    await db.refresh(user_db)

    return schemas.UpdateUserPutOut(
        first_name_one= user_db.first_name_one,
        first_name_two= user_db.first_name_two,
        last_name_one= user_db.last_name_one,
        last_name_two= user_db.last_name_two,
        email= user_db.email
    )