import json

import tables
from redis import asyncio as redis
from rediska import CacheRep
from RepClasses import DishRep, MenuRep, SubmenuRep
from sqlalchemy.ext.asyncio import AsyncSession


class MenuCRUD:
    def __init__(self, rep_session: AsyncSession, cache_loop: redis.Redis):
        self.menu_rep = MenuRep(rep_session)
        self.cache_rep = CacheRep(cache_loop)

    async def create_menu(self, data: tables.MenuSchema):
        menu = await self.menu_rep.create_menu(data)
        await self.cache_rep.set(f'menu_{menu.id}', menu.json())  # Add .json() here
        await self.cache_rep.delete('all_menus')
        return menu

    async def get_all_menus(self):
        cached_menus = await self.cache_rep.get('all_menus')
        if cached_menus:
            return [tables.MenuAll(**json.loads(menu)) for menu in json.loads(cached_menus)]

        menus = await self.menu_rep.get_all_menus()
        menus_data = [menu.json() for menu in menus]
        await self.cache_rep.set('all_menus', json.dumps(menus_data))

        return menus

    async def get_menu(self, menu_id: int):
        cached_menu = await self.cache_rep.get(f'menu_{menu_id}')
        if cached_menu:
            return tables.MenuAll(**json.loads(cached_menu))

        menu = await self.menu_rep.get_menu(menu_id)
        await self.cache_rep.set(f'menu_{menu_id}', menu.json())  # Add .json() here
        return menu

    async def update_menu(self, menu_id: int, data: tables.MenuSchema):
        updated_menu = await self.menu_rep.update_menu(menu_id, data)
        await self.cache_rep.set(f'menu_{menu_id}', updated_menu.json())  # Add .json() here
        await self.cache_rep.delete('all_menus')  # Clear all menus cache
        return updated_menu

    async def delete_menu(self, menu_id: int):
        deleted_menu = await self.menu_rep.delete_menu(menu_id)
        await self.cache_rep.delete('all_menus')
        await self.cache_rep.delete(f'menu_{menu_id}')
        await self.cache_rep.delete_by_pattern('dish_*')
        await self.cache_rep.delete_by_pattern('submenu_*')
        await self.cache_rep.delete(f'menu_submenus_{menu_id}')
        await self.cache_rep.delete_by_pattern('submenu_dishes_*')
        return deleted_menu


class SubmenuCRUD:
    def __init__(self, rep_session: AsyncSession, cache_loop: redis.Redis):
        self.submenu_rep = SubmenuRep(rep_session)
        self.cache_rep = CacheRep(cache_loop)

    async def create_submenu(self, menu_id: int, data: tables.SubmenuSchema):
        submenu = await self.submenu_rep.create_submenu(menu_id, data)
        await self.cache_rep.set(f'submenu_{submenu.id}', submenu.json())  # Add .json() here
        await self.cache_rep.delete(f'menu_submenus_{menu_id}')
        await self.cache_rep.delete(f'menu_{menu_id}')
        await self.cache_rep.delete('all_menus')
        return submenu

    async def get_submenu(self, submenu_id: int):
        cached_submenu = await self.cache_rep.get(f'submenu_{submenu_id}')
        if cached_submenu:
            return tables.SubmenuAll(**json.loads(cached_submenu))

        submenu = await self.submenu_rep.get_submenu(submenu_id)

        await self.cache_rep.set(f'submenu_{submenu_id}', submenu.json())  # Add .json() here
        return submenu

    async def get_all_submenus(self, menu_id: int):
        cached_submenus = await self.cache_rep.get(f'menu_submenus_{menu_id}')
        if cached_submenus:
            return [tables.SubmenuAll(**json.loads(submenu)) for submenu in json.loads(cached_submenus)]

        submenus = await self.submenu_rep.get_all_submenus(menu_id)
        submenus_data = [submenu.json() for submenu in submenus]
        await self.cache_rep.set(f'menu_submenus_{menu_id}', json.dumps(submenus_data))

        return submenus

    async def update_submenu(self, menu_id: int, submenu_id: int, data: tables.SubmenuSchema):
        updated_submenu = await self.submenu_rep.update_submenu(submenu_id, data)
        await self.cache_rep.set(f'submenu_{submenu_id}', updated_submenu.json())  # Add .json() here
        await self.cache_rep.delete(f'menu_submenus_{menu_id}')
        return updated_submenu

    async def delete_submenu(self, menu_id: int, submenu_id: int):
        submenu = await self.submenu_rep.delete_submenu(submenu_id)
        await self.cache_rep.delete(f'submenu_{submenu_id}')
        await self.cache_rep.delete(f'menu_submenus_{menu_id}')
        await self.cache_rep.delete(f'menu_{menu_id}')
        await self.cache_rep.delete('all_menus')
        await self.cache_rep.delete_by_pattern('dish_*')
        await self.cache_rep.delete(f'submenu_dishes_{submenu_id}')
        return submenu


class DishCRUD:
    def __init__(self, rep_session: AsyncSession, cache_loop: redis.Redis):
        self.dish_rep = DishRep(rep_session)
        self.cache_rep = CacheRep(cache_loop)

    async def create_dish(self, menu_id: int, submenu_id: int, data: tables.DishSchema):
        dish = await self.dish_rep.create_dish(submenu_id, data)
        await self.cache_rep.set(f'dish_{dish.id}', dish.json())  # Add .json() here
        await self.cache_rep.delete(f'submenu_dishes_{submenu_id}')  # Clear submenu dishes cache
        await self.cache_rep.delete(f'menu_{menu_id}')
        await self.cache_rep.delete(f'submenu_{submenu_id}')
        return dish

    async def get_dish(self, dish_id: int):
        cached_dish = await self.cache_rep.get(f'dish_{dish_id}')
        if cached_dish:
            return tables.DishAll(**json.loads(cached_dish))

        dish = await self.dish_rep.get_dish(dish_id)
        if not dish:
            return None

        await self.cache_rep.set(f'dish_{dish_id}', dish.json())  # Add .json() here
        return dish

    async def get_all_dishes(self, submenu_id: int):
        cached_dishes = await self.cache_rep.get(f'submenu_dishes_{submenu_id}')
        if cached_dishes:
            return [tables.DishAll(**json.loads(dish)) for dish in json.loads(cached_dishes)]

        dishes = await self.dish_rep.get_all_dishes(submenu_id)
        dishes_data = [dish.json() for dish in dishes]
        await self.cache_rep.set(f'submenu_dishes_{submenu_id}', json.dumps(dishes_data))

        return dishes

    async def update_dish(self, submenu_id: int, dish_id: int, data: tables.DishSchema):
        updated_dish = await self.dish_rep.update_dish(dish_id, data)
        await self.cache_rep.set(f'dish_{dish_id}', updated_dish.json())  # Add .json() here
        await self.cache_rep.delete(f'submenu_dishes_{submenu_id}')
        return updated_dish

    async def delete_dish(self, menu_id: int, submenu_id: int, dish_id: int):
        dish = await self.dish_rep.delete_dish(dish_id)

        await self.cache_rep.delete(f'dish_{dish_id}')
        await self.cache_rep.delete(f'submenu_dishes_{submenu_id}')
        await self.cache_rep.delete(f'menu_{menu_id}')
        await self.cache_rep.delete(f'submenu_{submenu_id}')
        await self.cache_rep.delete(f'menu_submenus_{menu_id}')
        await self.cache_rep.delete('all_menus')
        return dish
