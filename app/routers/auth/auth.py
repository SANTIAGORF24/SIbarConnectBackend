from fastapi import APIRouter, HTTPException, status, Depends
from core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.auth import auth as schemas
from services.auth import auth as authservices

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/login", response_model= schemas.LoginUserOut, status_code= status.HTTP_200_OK)
async def login_user(user_query: schemas.LoginUserData, db: AsyncSession = Depends(get_db)):
    return await authservices.Login_usuario(user_query, db)
