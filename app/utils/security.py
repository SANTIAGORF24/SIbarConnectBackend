from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verifi_password(plain_password: str, hased_password: str) -> str:
    return pwd_context.verify(plain_password, hased_password)
