import bcrypt

def hash_password(password: str) -> str:
    """
    Hashea una contraseña usando bcrypt.
    Si la contraseña es mayor a 72 bytes, la trunca (límite de bcrypt).
    """
    # Bcrypt tiene un límite de 72 bytes para contraseñas
    # Convertir a bytes y truncar si es necesario
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    
    # Generar salt y hashear la contraseña
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # Retornar como string (bcrypt almacena el hash como bytes)
    return hashed.decode('utf-8')

def verifi_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica una contraseña contra un hash.
    Retorna True si la contraseña coincide, False en caso contrario.
    """
    try:
        # Truncar la contraseña si es necesario
        password_bytes = plain_password.encode('utf-8')
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]
        
        # Convertir el hash a bytes si es string
        if isinstance(hashed_password, str):
            hashed_password_bytes = hashed_password.encode('utf-8')
        else:
            hashed_password_bytes = hashed_password
        
        # Verificar la contraseña
        return bcrypt.checkpw(password_bytes, hashed_password_bytes)
    except Exception as e:
        # Si hay algún error, retornar False
        return False
