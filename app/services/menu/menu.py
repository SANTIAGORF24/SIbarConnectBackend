from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
from models.menu import menu as models
from schemas.menu import menu as schemas
from typing import List, Optional

class MenuService:
    """Servicio para manejar todas las operaciones CRUD de menús"""
    
    async def create_menu(self, menu_data: schemas.MenuCreate, db: AsyncSession) -> models.Menu:
        """Crear un nuevo plato en el menú"""
        try:
            # Verificar si ya existe un plato con el mismo nombre en la misma mesa
            existing_menu = await db.execute(
                select(models.Menu).where(
                    models.Menu.nombre_plato == menu_data.nombre_plato,
                    models.Menu.mesa == menu_data.mesa
                )
            )
            if existing_menu.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ya existe un plato '{menu_data.nombre_plato}' para la mesa {menu_data.mesa}"
                )
            
            # Crear nuevo plato
            new_menu = models.Menu(
                nombre_plato=menu_data.nombre_plato,
                costo=menu_data.costo,
                mesa=menu_data.mesa
            )
            
            db.add(new_menu)
            await db.commit()
            await db.refresh(new_menu)
            
            return new_menu
            
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear el plato: {str(e)}"
            )
    
    async def get_menu_by_id(self, menu_id: int, db: AsyncSession) -> models.Menu:
        """Obtener un plato por su ID"""
        try:
            result = await db.execute(select(models.Menu).where(models.Menu.id == menu_id))
            menu = result.scalar_one_or_none()
            
            if not menu:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Plato con ID {menu_id} no encontrado"
                )
            
            return menu
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener el plato: {str(e)}"
            )
    
    async def get_all_menus(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[models.Menu]:
        """Obtener todos los platos del menú con paginación"""
        try:
            result = await db.execute(
                select(models.Menu)
                .order_by(models.Menu.mesa, models.Menu.nombre_plato)
                .offset(skip)
                .limit(limit)
            )
            return result.scalars().all()
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener los platos: {str(e)}"
            )
    
    async def get_menus_by_mesa(self, mesa: int, db: AsyncSession) -> List[models.Menu]:
        """Obtener todos los platos de una mesa específica"""
        try:
            result = await db.execute(
                select(models.Menu)
                .where(models.Menu.mesa == mesa)
                .order_by(models.Menu.nombre_plato)
            )
            menus = result.scalars().all()
            
            if not menus:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No se encontraron platos para la mesa {mesa}"
                )
            
            return menus
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener platos de la mesa: {str(e)}"
            )
    
    async def get_menus_by_costo_range(self, costo_min: float, costo_max: float, db: AsyncSession) -> List[models.Menu]:
        """Obtener platos dentro de un rango de costo"""
        try:
            result = await db.execute(
                select(models.Menu)
                .where(models.Menu.costo >= costo_min, models.Menu.costo <= costo_max)
                .order_by(models.Menu.costo)
            )
            menus = result.scalars().all()
            
            if not menus:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No se encontraron platos en el rango de costo ${costo_min} - ${costo_max}"
                )
            
            return menus
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener platos por rango de costo: {str(e)}"
            )
    
    async def update_menu_put(self, menu_id: int, menu_data: schemas.MenuUpdate, db: AsyncSession) -> models.Menu:
        """Actualizar completamente un plato (PUT)"""
        try:
            # Verificar que el plato existe
            menu = await self.get_menu_by_id(menu_id, db)
            
            # Verificar si ya existe otro plato con el mismo nombre en la misma mesa
            if menu_data.nombre_plato != menu.nombre_plato or menu_data.mesa != menu.mesa:
                existing_menu = await db.execute(
                    select(models.Menu).where(
                        models.Menu.nombre_plato == menu_data.nombre_plato,
                        models.Menu.mesa == menu_data.mesa,
                        models.Menu.id != menu_id
                    )
                )
                if existing_menu.scalar_one_or_none():
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Ya existe un plato '{menu_data.nombre_plato}' para la mesa {menu_data.mesa}"
                    )
            
            # Actualizar todos los campos
            menu.nombre_plato = menu_data.nombre_plato
            menu.costo = menu_data.costo
            menu.mesa = menu_data.mesa
            
            await db.commit()
            await db.refresh(menu)
            
            return menu
            
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al actualizar el plato: {str(e)}"
            )
    
    async def update_menu_patch(self, menu_id: int, menu_data: schemas.MenuPatch, db: AsyncSession) -> models.Menu:
        """Actualizar parcialmente un plato (PATCH)"""
        try:
            # Verificar que el plato existe
            menu = await self.get_menu_by_id(menu_id, db)
            
            # Actualizar solo los campos proporcionados
            update_data = menu_data.dict(exclude_unset=True)
            
            if not update_data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se proporcionaron campos para actualizar"
                )
            
            # Verificar duplicados si se está actualizando nombre o mesa
            if 'nombre_plato' in update_data or 'mesa' in update_data:
                new_nombre = update_data.get('nombre_plato', menu.nombre_plato)
                new_mesa = update_data.get('mesa', menu.mesa)
                
                if new_nombre != menu.nombre_plato or new_mesa != menu.mesa:
                    existing_menu = await db.execute(
                        select(models.Menu).where(
                            models.Menu.nombre_plato == new_nombre,
                            models.Menu.mesa == new_mesa,
                            models.Menu.id != menu_id
                        )
                    )
                    if existing_menu.scalar_one_or_none():
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Ya existe un plato '{new_nombre}' para la mesa {new_mesa}"
                        )
            
            # Aplicar las actualizaciones
            for field, value in update_data.items():
                setattr(menu, field, value)
            
            await db.commit()
            await db.refresh(menu)
            
            return menu
            
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al actualizar parcialmente el plato: {str(e)}"
            )
    
    async def delete_menu(self, menu_id: int, db: AsyncSession) -> dict:
        """Eliminar un plato del menú"""
        try:
            # Verificar que el plato existe
            menu = await self.get_menu_by_id(menu_id, db)
            
            await db.delete(menu)
            await db.commit()
            
            return {
                "message": f"Plato '{menu.nombre_plato}' eliminado exitosamente",
                "deleted_id": menu_id
            }
            
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al eliminar el plato: {str(e)}"
            )
    
    async def delete_menus_by_mesa(self, mesa: int, db: AsyncSession) -> dict:
        """Eliminar todos los platos de una mesa"""
        try:
            # Verificar que existen platos en esa mesa
            result = await db.execute(select(models.Menu).where(models.Menu.mesa == mesa))
            menus = result.scalars().all()
            
            if not menus:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No se encontraron platos para la mesa {mesa}"
                )
            
            # Eliminar todos los platos de la mesa
            await db.execute(delete(models.Menu).where(models.Menu.mesa == mesa))
            await db.commit()
            
            return {
                "message": f"Se eliminaron {len(menus)} platos de la mesa {mesa}",
                "deleted_count": len(menus),
                "mesa": mesa
            }
            
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al eliminar platos de la mesa: {str(e)}"
            )

# Instancia global del servicio
menu_service = MenuService()
