#importaciones principales del poryecto
import os 
from dotenv import load_dotenv #libreria estandar para leer archivos de entoro
from pydantic_settings import BaseSettings #Provee parsing y validacion tipada de valores que vienen del entorno (o de otros origenes)


#carga el archivo de variavbles de enotor
load_dotenv() 


class Settings(BaseSettings):
    app_name: str = os.getenv("APP_NAME")
    app_version: str = os.getenv("APP_VERSION")

    #Datos de la bd
    BD_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("BD_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: str = os.getenv("DB_PORT")
    DB_NAME: str = os.getenv("DB_NAME")