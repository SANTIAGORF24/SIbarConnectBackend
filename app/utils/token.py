from datetime import datetime, timedelta
from jose import jwt, JWTError
from core import Settings
from fastapi import HTTPException, status


SECRET_KEY= Settings().SECRET_KEY
ALGORITHM= Settings().ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES= Settings().ACCESS_TOKEN_EXPIRE_MINUTES

def Crear_acces_token(data:dict, expires_delta:int = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire = datetime.utcnow()+ timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """
    Verificar y decodificar un JWT token
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido: no se encontró el email",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return email
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
