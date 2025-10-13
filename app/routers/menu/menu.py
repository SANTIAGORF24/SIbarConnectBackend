from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from core.security import get_current_active_user
from models.users.user import User
from schemas.menu import menu as schemas
from services.menu import menu_service
from typing import List

router = APIRouter(
    prefix="/menu",
    tags=["menu"]
)

# ===== RUTAS POST (Crear) =====
@router.post("/create", response_model=schemas.MenuOut, status_code=status.HTTP_201_CREATED)
async def create_menu(
    menu_data: schemas.MenuCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Crear un nuevo plato en el menú (Requiere autenticación)
    
    - **nombre_plato**: Nombre del plato (máximo 100 caracteres)
    - **costo**: Costo del plato (debe ser mayor a 0)
    - **mesa**: Número de mesa (debe ser mayor a 0)
    """
    return await menu_service.create_menu(menu_data, db)

# ===== RUTAS GET (Leer) =====
@router.get("/all", response_model=List[schemas.MenuOut], status_code=status.HTTP_200_OK)
async def get_all_menus(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Límite de registros a retornar"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener todos los platos del menú con paginación (Requiere autenticación)
    
    - **skip**: Número de registros a saltar (para paginación)
    - **limit**: Máximo número de registros a retornar
    """
    return await menu_service.get_all_menus(db, skip, limit)

@router.get("/id/{menu_id}", response_model=schemas.MenuOut, status_code=status.HTTP_200_OK)
async def get_menu_by_id(
    menu_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener un plato específico por su ID (Requiere autenticación)
    
    - **menu_id**: ID único del plato
    """
    return await menu_service.get_menu_by_id(menu_id, db)

@router.get("/mesa/{mesa}", response_model=List[schemas.MenuOut], status_code=status.HTTP_200_OK)
async def get_menus_by_mesa(
    mesa: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener todos los platos de una mesa específica (Requiere autenticación)
    
    - **mesa**: Número de mesa
    """
    return await menu_service.get_menus_by_mesa(mesa, db)

@router.post("/mesa", response_model=List[schemas.MenuOut], status_code=status.HTTP_200_OK)
async def get_menus_by_mesa_post(
    mesa_data: schemas.MenuByMesa,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener todos los platos de una mesa específica usando POST (Requiere autenticación)
    
    - **mesa**: Número de mesa
    """
    return await menu_service.get_menus_by_mesa(mesa_data.mesa, db)

@router.post("/costo-range", response_model=List[schemas.MenuOut], status_code=status.HTTP_200_OK)
async def get_menus_by_costo_range(
    costo_range: schemas.MenuByCostoRange,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener platos dentro de un rango de costo (Requiere autenticación)
    
    - **costo_min**: Costo mínimo
    - **costo_max**: Costo máximo (debe ser mayor al mínimo)
    """
    return await menu_service.get_menus_by_costo_range(
        costo_range.costo_min, 
        costo_range.costo_max, 
        db
    )

@router.get("/costo-range", response_model=List[schemas.MenuOut], status_code=status.HTTP_200_OK)
async def get_menus_by_costo_range_get(
    costo_min: float = Query(..., ge=0, description="Costo mínimo"),
    costo_max: float = Query(..., gt=0, description="Costo máximo"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener platos dentro de un rango de costo usando GET (Requiere autenticación)
    
    - **costo_min**: Costo mínimo
    - **costo_max**: Costo máximo
    """
    if costo_max <= costo_min:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El costo máximo debe ser mayor al costo mínimo"
        )
    
    return await menu_service.get_menus_by_costo_range(costo_min, costo_max, db)

# ===== RUTAS PUT (Actualización completa) =====
@router.put("/update/{menu_id}", response_model=schemas.MenuOut, status_code=status.HTTP_200_OK)
async def update_menu_put(
    menu_id: int,
    menu_data: schemas.MenuUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Actualizar completamente un plato del menú PUT (Requiere autenticación)
    
    - **menu_id**: ID único del plato a actualizar
    - **nombre_plato**: Nuevo nombre del plato
    - **costo**: Nuevo costo del plato
    - **mesa**: Nueva mesa asignada
    """
    return await menu_service.update_menu_put(menu_id, menu_data, db)

# ===== RUTAS PATCH (Actualización parcial) =====
@router.patch("/update/{menu_id}", response_model=schemas.MenuOut, status_code=status.HTTP_200_OK)
async def update_menu_patch(
    menu_id: int,
    menu_data: schemas.MenuPatch,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Actualizar parcialmente un plato del menú PATCH (Requiere autenticación)
    
    - **menu_id**: ID único del plato a actualizar
    - Campos opcionales a actualizar:
        - **nombre_plato**: Nuevo nombre del plato
        - **costo**: Nuevo costo del plato  
        - **mesa**: Nueva mesa asignada
    """
    return await menu_service.update_menu_patch(menu_id, menu_data, db)

# ===== RUTAS DELETE (Eliminar) =====
@router.delete("/delete/{menu_id}", status_code=status.HTTP_200_OK)
async def delete_menu(
    menu_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Eliminar un plato específico del menú (Requiere autenticación)
    
    - **menu_id**: ID único del plato a eliminar
    """
    return await menu_service.delete_menu(menu_id, db)

@router.delete("/delete/mesa/{mesa}", status_code=status.HTTP_200_OK)
async def delete_menus_by_mesa(
    mesa: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Eliminar todos los platos de una mesa específica (Requiere autenticación)
    
    - **mesa**: Número de mesa cuyos platos serán eliminados
    """
    return await menu_service.delete_menus_by_mesa(mesa, db)
