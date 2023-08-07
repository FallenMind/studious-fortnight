import tables
from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, subqueryload


class MenuRep:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_menu(self, menu_data: tables.MenuSchema):
        menu_data_dict = menu_data.model_dump(exclude={'id'})
        menu = tables.Menu(**menu_data_dict)
        self.session.add(menu)
        await self.session.commit()
        await self.session.refresh(menu)

        menu_data_all = tables.MenuAll(
            id=str(menu.id),
            title=menu.title,
            description=menu.description,
            submenus_count=0,
            dishes_count=0,
        )

        return menu_data_all

    async def get_all_menus(self):
        query = select(tables.Menu).options(subqueryload(tables.Menu.submenus),
                                            subqueryload(tables.Menu.submenus, tables.Submenu.dishes)).distinct()
        result = await self.session.execute(query)

        menus_data = []
        for menu in result.scalars().all():
            submenu_count = len(menu.submenus)
            dish_count = sum(len(submenu.dishes) for submenu in menu.submenus)

            menu_data = tables.MenuAll(
                id=str(menu.id),
                title=menu.title,
                description=menu.description,
                submenus_count=submenu_count,
                dishes_count=dish_count,
            )
            menus_data.append(menu_data)

        return menus_data

    async def get_menu(self, menu_id):
        menu = await self.session.get(tables.Menu, menu_id)
        if menu:
            query_submenus_count = select(func.count(tables.Submenu.id)).where(tables.Submenu.menu_id == menu_id)
            result_submenus_count = await self.session.execute(query_submenus_count)
            submenu_count = result_submenus_count.scalar()

            query_dishes_count = select(func.count(tables.Dish.id)).join(tables.Submenu).where(
                tables.Submenu.menu_id == menu_id)
            result_dishes_count = await self.session.execute(query_dishes_count)
            dish_count = result_dishes_count.scalar()

            return tables.MenuAll(
                id=str(menu.id),
                title=menu.title,
                description=menu.description,
                submenus_count=submenu_count,
                dishes_count=dish_count,
            )
        else:
            raise HTTPException(status_code=404, detail='menu not found')

    async def update_menu(self, menu_id: int, updated_menu: tables.MenuSchema):
        menu = await self.session.get(tables.Menu, menu_id)
        if menu:
            menu.title = updated_menu.title
            menu.description = updated_menu.description

            query_submenus_count = select(func.count(tables.Submenu.id)).where(tables.Submenu.menu_id == menu_id)
            result_submenus_count = await self.session.execute(query_submenus_count)
            submenu_count = result_submenus_count.scalar()

            query_dishes_count = select(func.count(tables.Dish.id)).join(tables.Submenu).where(
                tables.Submenu.menu_id == menu_id)
            result_dishes_count = await self.session.execute(query_dishes_count)
            dish_count = result_dishes_count.scalar()

            await self.session.commit()
            await self.session.refresh(menu)
            return tables.MenuAll(
                id=str(menu.id),
                title=menu.title,
                description=menu.description,
                submenus_count=submenu_count,
                dishes_count=dish_count,
            )
        else:
            raise HTTPException(status_code=404, detail='menu not found')

    async def delete_menu(self, menu_id):
        menu = await self.session.get(tables.Menu, menu_id)
        if menu:
            await self.session.delete(menu)
            await self.session.commit()
            return {'message': 'Menu deleted successfully.'}
        else:
            raise HTTPException(status_code=404, detail='menu not found')


class SubmenuRep:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_submenu(self, submenu: tables.SubmenuSchema, menu_id: int):
        menu = await self.session.get(tables.Menu, menu_id)
        if not menu:
            raise HTTPException(status_code=404, detail='Menu not found.')
        submenu_dict = submenu.model_dump(exclude={'id'})
        submenu_dict['menu_id'] = menu_id
        submenu_data = tables.Submenu(**submenu_dict)
        self.session.add(submenu_data)
        await self.session.commit()
        await self.session.refresh(submenu_data)
        query = select(func.count(tables.Dish.id)).where(tables.Dish.submenu_id == submenu_data.id)
        result = await self.session.execute(query)
        dish_count = result.scalar()
        return tables.SubmenuAll(
            id=str(submenu_data.id),
            title=submenu_data.title,
            description=submenu_data.description,
            dishes_count=dish_count
        )

    async def get_all_submenus(self, menu_id: int):
        query = select(tables.Submenu).options(joinedload(tables.Submenu.dishes)).where(
            tables.Submenu.menu_id == menu_id
        ).distinct()
        result = await self.session.execute(query)
        submenus = result.unique().scalars().all()
        submenu_data_list = []
        for submenu in submenus:
            dish_count = len(submenu.dishes) if submenu.dishes else 0
            submenu_data = tables.SubmenuAll(
                id=str(submenu.id),
                title=submenu.title,
                description=submenu.description,
                dishes_count=dish_count
            )
            submenu_data_list.append(submenu_data)
        return submenu_data_list

    async def get_submenu(self, submenu_id: int):
        query = select(tables.Submenu).options(subqueryload(tables.Submenu.dishes)).where(
            tables.Submenu.id == submenu_id)
        result = await self.session.execute(query)
        submenu = result.scalars().one_or_none()
        if submenu:
            dish_count = len(submenu.dishes) if submenu.dishes else 0
            submenu_data = tables.SubmenuAll(
                id=str(submenu.id),
                title=submenu.title,
                description=submenu.description,
                dishes_count=dish_count
            )
            return submenu_data
        else:
            raise HTTPException(status_code=404, detail='submenu not found')

    async def update_menu(self, menu_id: int, updated_menu: tables.MenuSchema):
        menu = await self.session.get(tables.Menu, menu_id)
        if menu:
            menu.title = updated_menu.title
            menu.description = updated_menu.description

            await self.session.commit()
            await self.session.refresh(menu)
            return tables.MenuAll(
                id=str(menu.id),
                title=menu.title,
                description=menu.description
            )

    async def update_submenu(self, submenu_id: int, updated_submenu: tables.SubmenuSchema):
        query = select(tables.Submenu).options(subqueryload(tables.Submenu.dishes)).where(
            tables.Submenu.id == submenu_id)
        result = await self.session.execute(query)
        submenu = result.scalars().one_or_none()
        if not submenu:
            raise HTTPException(status_code=404, detail='Submenu not found.')

        submenu.title = updated_submenu.title
        submenu.description = updated_submenu.description
        dish_count = len(submenu.dishes) if submenu.dishes else 0
        await self.session.commit()
        await self.session.refresh(submenu)

        return tables.SubmenuAll(
            id=str(submenu.id),
            title=submenu.title,
            description=submenu.description,
            dishes_count=dish_count
        )

    async def delete_submenu(self, submenu_id):
        submenu = await self.session.get(tables.Submenu, submenu_id)
        if submenu:
            await self.session.delete(submenu)
            await self.session.commit()
            return {'message': 'Submenu deleted successfully.'}
        else:
            raise HTTPException(status_code=404, detail='Submenu not found.')


class DishRep:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_dish(self, dish_data: tables.DishSchema, submenu_id: int):
        dish_data_dict = dish_data.model_dump()
        dish_data_dict['submenu_id'] = submenu_id
        dish = tables.Dish(**dish_data_dict)
        self.session.add(dish)
        await self.session.commit()
        await self.session.refresh(dish)
        return tables.DishAll(
            id=str(dish.id),
            title=dish.title,
            description=dish.description,
            price=str(dish.price)
        )

    async def get_all_dishes(self, submenu_id):
        query = select(tables.Dish).where(
            tables.Dish.submenu_id == submenu_id
        )
        result = await self.session.execute(query)
        dishes = []
        for dish in result.scalars().all():
            dish_data = tables.DishAll(
                id=str(dish.id),
                title=dish.title,
                description=dish.description,
                price=str(dish.price)
            )
            dishes.append(dish_data)
        return dishes

    async def get_dish(self, dish_id):
        dish = await self.session.get(tables.Dish, dish_id)
        if dish:
            return tables.DishAll(
                id=str(dish.id),
                title=dish.title,
                description=dish.description,
                price=str(dish.price)
            )
        else:
            raise HTTPException(status_code=404, detail='dish not found')

    async def update_dish(self, dish_id: int, updated_dish: tables.DishSchema):
        dish = await self.session.get(tables.Dish, dish_id)
        if dish:
            for field, value in updated_dish.model_dump().items():
                setattr(dish, field, value)
            await self.session.commit()
            await self.session.refresh(dish)
            return tables.DishAll(
                id=str(dish.id),
                title=dish.title,
                description=dish.description,
                price=str(dish.price)
            )
        else:
            raise HTTPException(status_code=404, detail='dish not found')

    async def delete_dish(self, dish_id):
        dish = await self.session.get(tables.Dish, dish_id)
        if dish:
            await self.session.delete(dish)
            await self.session.commit()
            return {'message': 'Dish deleted successfully.'}
        else:
            raise HTTPException(status_code=404, detail='dish not found')
