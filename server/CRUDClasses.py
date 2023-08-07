from pydantic import ValidationError

from RepClasses import MenuRep, SubmenuRep, DishRep
from rediska import CacheRep
import tables


class MenuCRUD:
    def __init__(self, rep_session, cache_loop):
        self.menu_rep = MenuRep(rep_session)
        self.cache_rep = CacheRep(cache_loop)

    async def create_menu(self, data):
        try:
            menu = await self.menu_rep.create_menu(data)
            await self.cache_rep.set(f"menu_{menu.id}", menu.json())
            await self.cache_rep.delete("all_menus")
            return menu
        except ValidationError:
            raise ValueError("Invalid menu data")

    async def get_all_menus(self):
        cached_menus = await self.cache_rep.get("all_menus")
        if cached_menus:
            return [tables.MenuAll(**menu) for menu in cached_menus]

        menus = await self.menu_rep.get_all_menus()
        await self.cache_rep.set("all_menus", [menu.json() for menu in menus])
        return menus

    async def get_menu(self, menu_id):
        cached_menu = await self.cache_rep.get(f"menu_{menu_id}")
        if cached_menu:
            return tables.MenuAll(**cached_menu)

        menu = await self.menu_rep.get_menu(menu_id)
        if not menu:
            return None

        await self.cache_rep.set(f"menu_{menu_id}", menu.json())
        return menu

    async def update_menu(self, menu_id, data):
        try:
            updated_menu = await self.menu_rep.update_menu(menu_id, data)
            await self.cache_rep.set(f"menu_{menu_id}", updated_menu.json())
            await self.cache_rep.delete("all_menus")  # Clear all menus cache
            return updated_menu
        except ValidationError:
            raise ValueError("Invalid menu data")

    async def delete_menu(self, menu_id):
        deleted_menu = await self.menu_rep.delete_menu(menu_id)
        await self.cache_rep.delete(f"menu_{menu_id}")
        await self.cache_rep.delete("all_menus")  # Clear all menus cache
        return deleted_menu


class SubmenuCRUD:
    def __init__(self, rep_session, cache_loop):
        self.submenu_rep = SubmenuRep(rep_session)
        self.cache_rep = CacheRep(cache_loop)

    async def create_submenu(self, menu_id, data):
        try:
            submenu = await self.submenu_rep.create_submenu(menu_id, data)
            await self.cache_rep.set(f"submenu_{submenu.id}", submenu.json())
            await self.cache_rep.delete(f"menu_submenus_{menu_id}")  # Clear menu submenus cache
            return submenu
        except ValidationError:
            raise ValueError("Invalid submenu data")

    async def get_submenu(self, submenu_id):
        cached_submenu = await self.cache_rep.get(f"submenu_{submenu_id}")
        if cached_submenu:
            return tables.SubmenuAll(**cached_submenu)

        submenu = await self.submenu_rep.get_submenu(submenu_id)
        if not submenu:
            return None

        await self.cache_rep.set(f"submenu_{submenu_id}", submenu.json())
        return submenu

    async def get_all_submenus(self, menu_id):
        cached_submenus = await self.cache_rep.get(f"menu_submenus_{menu_id}")
        if cached_submenus:
            return [tables.SubmenuAll(**submenu) for submenu in cached_submenus]

        submenus = await self.submenu_rep.get_all_submenus(menu_id)
        await self.cache_rep.set(f"menu_submenus_{menu_id}", [submenu.json() for submenu in submenus])
        return submenus

    async def update_submenu(self, submenu_id, data):
        try:
            updated_submenu = await self.submenu_rep.update_submenu(submenu_id, data)
            await self.cache_rep.set(f"submenu_{submenu_id}", updated_submenu.json())
            await self.cache_rep.delete(f"menu_submenus_{updated_submenu.menu_id}")  # Clear menu submenus cache
            return updated_submenu
        except ValidationError:
            raise ValueError("Invalid submenu data")

    async def delete_submenu(self, submenu_id):
        submenu = await self.get_submenu(submenu_id)
        if not submenu:
            return None

        await self.submenu_rep.delete_submenu(submenu_id)
        await self.cache_rep.delete(f"submenu_{submenu_id}")
        await self.cache_rep.delete(f"menu_submenus_{submenu.menu_id}")  # Clear menu submenus cache
        return submenu


class DishCRUD:
    def __init__(self, rep_session, cache_loop):
        self.dish_rep = DishRep(rep_session)
        self.cache_rep = CacheRep(cache_loop)

    async def create_dish(self, submenu_id, data):
        try:
            dish = await self.dish_rep.create_dish(submenu_id, data)
            await self.cache_rep.set(f"dish_{dish.id}", dish.json())
            await self.cache_rep.delete(f"submenu_dishes_{submenu_id}")  # Clear submenu dishes cache
            return dish
        except ValidationError:
            raise ValueError("Invalid dish data")

    async def get_dish(self, dish_id):
        cached_dish = await self.cache_rep.get(f"dish_{dish_id}")
        if cached_dish:
            return tables.DishAll(**cached_dish)

        dish = await self.dish_rep.get_dish(dish_id)
        if not dish:
            return None

        await self.cache_rep.set(f"dish_{dish_id}", dish.json())
        return dish

    async def get_all_dishes(self, submenu_id):
        cached_dishes = await self.cache_rep.get(f"submenu_dishes_{submenu_id}")
        if cached_dishes:
            return [tables.DishAll(**dish) for dish in cached_dishes]

        dishes = await self.dish_rep.get_all_dishes(submenu_id)
        await self.cache_rep.set(f"submenu_dishes_{submenu_id}", [dish.json() for dish in dishes])
        return dishes

    async def update_dish(self, dish_id, data):
        try:
            updated_dish = await self.dish_rep.update_dish(dish_id, data)
            await self.cache_rep.set(f"dish_{dish_id}", updated_dish.json())
            await self.cache_rep.delete(f"submenu_dishes_{updated_dish.submenu_id}")  # Clear submenu dishes cache
            return updated_dish
        except ValidationError:
            raise ValueError("Invalid dish data")

    async def delete_dish(self, dish_id):
        dish = await self.get_dish(dish_id)
        if not dish:
            return None

        await self.dish_rep.delete_dish(dish_id)
        await self.cache_rep.delete(f"dish_{dish_id}")
        await self.cache_rep.delete(f"submenu_dishes_{dish.submenu_id}")  # Clear submenu dishes cache
        return dish
