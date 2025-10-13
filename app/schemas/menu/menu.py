from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

# Schema base para Menu
class MenuBase(BaseModel):
    nombre_plato: str = Field(..., min_length=1, max_length=100, description="Nombre del plato")
    costo: float = Field(..., gt=0, description="Costo del plato en pesos")
    mesa: int = Field(..., gt=0, description="Número de mesa")

# Schema para crear un nuevo menu
class MenuCreate(MenuBase):
    @validator('nombre_plato')
    def validate_nombre_plato(cls, v):
        if not v.strip():
            raise ValueError('El nombre del plato no puede estar vacío')
        return v.strip().title()
    
    @validator('costo')
    def validate_costo(cls, v):
        if v <= 0:
            raise ValueError('El costo debe ser mayor a 0')
        return round(v, 2)

# Schema para actualización completa (PUT)
class MenuUpdate(MenuBase):
    @validator('nombre_plato')
    def validate_nombre_plato(cls, v):
        if not v.strip():
            raise ValueError('El nombre del plato no puede estar vacío')
        return v.strip().title()
    
    @validator('costo')
    def validate_costo(cls, v):
        if v <= 0:
            raise ValueError('El costo debe ser mayor a 0')
        return round(v, 2)

# Schema para actualización parcial (PATCH)
class MenuPatch(BaseModel):
    nombre_plato: Optional[str] = Field(None, min_length=1, max_length=100, description="Nombre del plato")
    costo: Optional[float] = Field(None, gt=0, description="Costo del plato en pesos")
    mesa: Optional[int] = Field(None, gt=0, description="Número de mesa")
    
    @validator('nombre_plato')
    def validate_nombre_plato(cls, v):
        if v is not None and not v.strip():
            raise ValueError('El nombre del plato no puede estar vacío')
        return v.strip().title() if v else v
    
    @validator('costo')
    def validate_costo(cls, v):
        if v is not None and v <= 0:
            raise ValueError('El costo debe ser mayor a 0')
        return round(v, 2) if v else v

# Schema para respuesta
class MenuOut(MenuBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Schema para consultar platos por mesa
class MenuByMesa(BaseModel):
    mesa: int = Field(..., gt=0, description="Número de mesa")

# Schema para consultar platos por rango de costo
class MenuByCostoRange(BaseModel):
    costo_min: float = Field(..., ge=0, description="Costo mínimo")
    costo_max: float = Field(..., gt=0, description="Costo máximo")
    
    @validator('costo_max')
    def validate_costo_range(cls, v, values):
        if 'costo_min' in values and v <= values['costo_min']:
            raise ValueError('El costo máximo debe ser mayor al costo mínimo')
        return v
