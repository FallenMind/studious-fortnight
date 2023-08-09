import os

import CRUDClasses
import tables
from fastapi import Depends, FastAPI
from redis import asyncio as redis
from settings import database_name, host, password, port, username
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

engine_link = os.environ.get('DATABASE_URL')  # {username}:{password}@{host}:{port}/{database_name}
test_check = os.environ.get('TEST_CHECK')

if engine_link:
    engine = create_async_engine(f'postgresql+asyncpg://{engine_link}')
else:
    engine = create_async_engine(f'postgresql+asyncpg://{username}:{password}@{host}:{port}/{database_name}')
app = FastAPI()
redis_con: redis.Redis


async def get_session():
    async with AsyncSession(engine) as session:
        yield session


@app.post('/api/v1/menus', response_model=tables.MenuAll, status_code=201)
async def create_menu(menu: tables.MenuSchema, session: AsyncSession = Depends(get_session)):
    menu_crud = CRUDClasses.MenuCRUD(session, redis_con)
    return await menu_crud.create_menu(menu)


@app.get('/api/v1/menus/{menu_id}', response_model=tables.MenuAll)
async def read_menu(menu_id: int, session: AsyncSession = Depends(get_session)):
    menu_crud = CRUDClasses.MenuCRUD(session, redis_con)
    return await menu_crud.get_menu(menu_id)


@app.patch('/api/v1/menus/{menu_id}', response_model=tables.MenuAll)
async def update_menu(menu_id: int, updated_menu: tables.MenuSchema, session: AsyncSession = Depends(get_session)):
    menu_crud = CRUDClasses.MenuCRUD(session, redis_con)
    return await menu_crud.update_menu(menu_id, updated_menu)


@app.delete('/api/v1/menus/{menu_id}')
async def delete_menu(menu_id: int, session: AsyncSession = Depends(get_session)):
    menu_crud = CRUDClasses.MenuCRUD(session, redis_con)
    return await menu_crud.delete_menu(menu_id)


@app.get('/api/v1/menus', response_model=list[tables.MenuAll])
async def get_all_menus(session: AsyncSession = Depends(get_session)):
    menu_crud = CRUDClasses.MenuCRUD(session, redis_con)
    return await menu_crud.get_all_menus()


@app.post('/api/v1/menus/{menu_id}/submenus/', response_model=tables.SubmenuAll, status_code=201)
async def create_submenu(menu_id: int, submenu: tables.SubmenuSchema, session: AsyncSession = Depends(get_session)):
    submenu_crud = CRUDClasses.SubmenuCRUD(session, redis_con)
    return await submenu_crud.create_submenu(menu_id, submenu)


@app.get('/api/v1/menus/{menu_id}/submenus/', response_model=list[tables.SubmenuAll])
async def get_all_submenus(menu_id: int, session: AsyncSession = Depends(get_session)):
    submenu_crud = CRUDClasses.SubmenuCRUD(session, redis_con)
    return await submenu_crud.get_all_submenus(menu_id)


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}', response_model=tables.SubmenuAll)
async def read_submenu(submenu_id: int, session: AsyncSession = Depends(get_session)):
    submenu_crud = CRUDClasses.SubmenuCRUD(session, redis_con)
    return await submenu_crud.get_submenu(submenu_id)


@app.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}', response_model=tables.SubmenuAll)
async def update_submenu(submenu_id: int, menu_id: int, updated_submenu: tables.SubmenuSchema,
                         session: AsyncSession = Depends(get_session)):
    submenu_crud = CRUDClasses.SubmenuCRUD(session, redis_con)
    return await submenu_crud.update_submenu(menu_id, submenu_id, updated_submenu)


@app.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
async def delete_submenu(submenu_id: int, menu_id: int, session: AsyncSession = Depends(get_session)):
    submenu_crud = CRUDClasses.SubmenuCRUD(session, redis_con)
    return await submenu_crud.delete_submenu(menu_id, submenu_id)


@app.post('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/', response_model=tables.DishAll, status_code=201)
async def create_dish(menu_id: int, submenu_id: int, dish: tables.DishSchema,
                      session: AsyncSession = Depends(get_session)):
    dish_crud = CRUDClasses.DishCRUD(session, redis_con)
    return await dish_crud.create_dish(menu_id, submenu_id, dish)


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/', response_model=list[tables.DishAll])
async def get_all_dishes(submenu_id: int, session: AsyncSession = Depends(get_session)):
    dish_crud = CRUDClasses.DishCRUD(session, redis_con)
    return await dish_crud.get_all_dishes(submenu_id)


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=tables.DishAll)
async def read_dish(dish_id: int, session: AsyncSession = Depends(get_session)):
    dish_crud = CRUDClasses.DishCRUD(session, redis_con)
    return await dish_crud.get_dish(dish_id)


@app.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=tables.DishAll)
async def update_dish(dish_id: int, submenu_id: int, updated_dish: tables.DishSchema,
                      session: AsyncSession = Depends(get_session)):
    dish_crud = CRUDClasses.DishCRUD(session, redis_con)
    return await dish_crud.update_dish(submenu_id, dish_id, updated_dish)


@app.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
async def delete_dish(dish_id: int, submenu_id: int, menu_id: int, session: AsyncSession = Depends(get_session)):
    dish_crud = CRUDClasses.DishCRUD(session, redis_con)
    return await dish_crud.delete_dish(menu_id, submenu_id, dish_id)


@app.get('/health')
async def health_check():
    return {'status': 'ok'}


@app.get('/death')
async def delete_all_data():
    if test_check == 'YES_I_WANT_TO_DELETE_MY_DATA':
        async with AsyncSession(engine) as session:
            await session.execute(delete(tables.Dish))
            await session.execute(delete(tables.Submenu))
            await session.execute(delete(tables.Menu))
            await session.commit()
        return {'status': 'died in pepperonis'}
    return {'status': 'no u'}


@app.on_event('startup')
async def startup_event():
    global redis_con
    await tables.create_tables(engine, test_check)
    if engine_link:
        try:
            redis_con = await redis.Redis(host='cache', port=6379)
            if not await redis_con.ping():
                raise Exception('Failed to connect to Redis cache')
        except Exception as e:
            raise Exception('Failed to initialize Redis connection') from e
    else:
        redis_con = await redis.Redis(host='localhost', port=6380)


@app.on_event('shutdown')
async def shutdown_event():
    await redis_con.close()
