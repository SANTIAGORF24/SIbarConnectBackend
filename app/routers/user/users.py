from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from core.security import get_current_active_user
from utils.security import hash_password
from models.users import user as models
from schemas.user import user as schemas
from sqlalchemy import select
from services.users import users as servicesuser

router = APIRouter(
    prefix="/user",
    tags=["users"]
)

@router.post("/create", response_model= schemas.UserOut, status_code=status.HTTP_201_CREATED) 
async def create_user(
    user: schemas.UserCreate, 
    db: AsyncSession = Depends(get_db)
):
    return await servicesuser.create_user_in_bd(user, db)

@router.get("/infouser/{user_id}", response_model=schemas.UserInfo, status_code=status.HTTP_200_OK)
async def info_user(
    user_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    return await servicesuser.consultar_usuario_por_id(user_id, db)

@router.post("/infouser", response_model= schemas.UserInfo, status_code=status.HTTP_200_OK)
async def info_user_mail(
    email_user: schemas.UserInfoName, 
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    return await servicesuser.obtener_usuario_por_email(email_user, db)

@router.delete("/deleteuser/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(
    user_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    return await servicesuser.eliminar_usuario_por_id(user_id, db)

@router.delete("/deleteuserforemail", status_code=status.HTTP_200_OK)
async def delete_user_for_email(
    request: schemas.DeleteUserForEmail,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    return await servicesuser.eliminar_usuario_por_email(request, db)

@router.put("/updateput/{user_id}", response_model= schemas.UpdateUserPutOut, status_code=status.HTTP_200_OK)
async def Update_user_put(
    user_id: int,
    user_data: schemas.UpdateUserPut,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    return await servicesuser.actualizar_usuario_put(user_id, user_data, db)