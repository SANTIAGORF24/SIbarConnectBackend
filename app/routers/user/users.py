from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from utils.security import hash_password
from models.users import user as models
from schemas.user import user as schemas
from sqlalchemy import select

router = APIRouter(
    prefix="/user",
    tags=["users"]
)


#ruta para crear el usuario 
#creamos la ruta con metodo post para mandar datos, la repsuesta se va a conertie en el esquea userOut, y si es todo correcto va a devovler el staus code 201
@router.post("/create", response_model= schemas.UserOut, status_code=status.HTTP_201_CREATED) 
#usamos una funcion asincrona ya que esto permite hacer diversas solcicitudes al backned
#vamos a usar el esqema de crear usuarios, y aparter recibe de dbuser, la sesion asincrona para poder conectarse
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    
    #1 VERIFICAR SI EL EMAIL EXISTE
    
    stmt = select(models.User).where(models.User.email == user.email)
    result = await db.execute(stmt)
    db_user = result.scalar_one_or_none()
    if db_user: 
        raise HTTPException(status_code=400, detail="email ya existe")   
        
    hash_pw = hash_password(user.password)

    new_user = models.User (
        fist_name_one = user.fist_name_one,
        fist_name_two = user.fist_name_two,
        last_name_one = user.last_name_one,
        last_name_two = user.last_name_two,
        email = user.email,
        Password_hash = hash_pw

    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)  # para obtener el ID generado

    # 5. Devolver el usuario (sin contraseña)
    return new_user


#ruta para obtener la informacion del usuario

@router.get("/infouser/{user_id}", response_model=schemas.UserInfo, status_code=status.HTTP_200_OK)
async def info_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.User).where(models.User.id == user_id)

    )
    user_bd = result.scalar_one_or_none()


    # Manejo de error por si el usuario no se encontro
    if user_bd is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    

    #Armamos el full name desde la instancia de la bd
    fullname = " ".join(filter(None, [
        getattr(user_bd, "fist_name_one", None),
        getattr(user_bd, "fist_name_two", None),
        getattr(user_bd, "last_name_one", None),
        getattr(user_bd, "last_name_two", None)
    ]))

    #devolvemos el esquema
    return schemas.UserInfo(
        id = user_bd.id,
        email = user_bd.email,
        fullname = fullname
    )

