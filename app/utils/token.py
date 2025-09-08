from datetime import datetime, timedelta
from jose import jwt
from core import Settings


SECRET_KEY= Settings().SECRET_KEY
ALGORITHM= Settings().ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES= Settings().ACCESS_TOKEN_EXPIRE_MINUTES

def Crear_acces_token(data:dict, expires_delta:int = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire = datetime.utcnow()+ timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
