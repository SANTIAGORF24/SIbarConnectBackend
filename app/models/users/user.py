from sqlalchemy import Column, Integer, String, Boolean
from core.database import Base

class User(Base):
    __tablename__="users"

    id = Column(Integer, primary_key=True, index=True)
    is_super_admin= Column(Boolean, nullable=False, default=False)
    first_name_one= Column(String(20), nullable=False)
    first_name_two= Column(String(20), nullable=True)
    last_name_one= Column(String(20), nullable=False)
    last_name_two= Column(String(20), nullable=False)
    email= Column(String(50), nullable=False)
    is_active= Column(Boolean, nullable=False, default=True)
    Password_hash= Column(String(255), nullable=False)     