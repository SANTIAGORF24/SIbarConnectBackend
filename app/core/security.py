from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.database import get_db
from models.users.user import User
from utils.token import verify_token

# Configurar el esquema de seguridad Bearer
security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Obtener el usuario actual basado en el JWT token
    """
    # Extraer el token del header Authorization
    token = credentials.credentials
    
    # Verificar y decodificar el token
    email = verify_token(token)
    
    # Buscar el usuario en la base de datos
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Obtener el usuario actual y verificar que esté activo
    """
    # Aquí puedes agregar lógica adicional para verificar si el usuario está activo
    # Por ejemplo, si tienes un campo 'is_active' en tu modelo User
    return current_user
