from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from core.database import Base

class Menu(Base):
    __tablename__ = "menus"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_plato = Column(String(100), nullable=False, index=True)
    costo = Column(Float, nullable=False)
    mesa = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Menu(id={self.id}, nombre_plato='{self.nombre_plato}', costo={self.costo}, mesa={self.mesa})>"
