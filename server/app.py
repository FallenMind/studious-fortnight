from typing import List


from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import delete

import CRUDClasses
import tables
from settings import username, password, host, port, database_name
import os

engine_link = os.environ.get("DATABASE_URL")  # {username}:{password}@{host}:{port}/{database_name}
test_check = os.environ.get("TEST_CHECK")

if engine_link:
    engine = create_async_engine(f"postgresql+asyncpg://{engine_link}")
else:
    engine = create_async_engine(f"postgresql+asyncpg://{username}:{password}@{host}:{port}/{database_name}")
app = FastAPI()
redis_pool = None


async def get_session():
    async with AsyncSession(engine) as session:
        yield session


@app.post("/api/v1/menus", response_model=tables.MenuAll, status_code=201)
async def create_menu(menu: tables.MenuSchema, session: AsyncSession = Depends(get_session)):
    menu_crud = CRUDClasses.MenuCRUD(session, redis_pool)
    return await menu_crud.create_menu(menu)


@app.get("/api/v1/menus/{menu_id}", response_model=tables.MenuAll)
async def read_menu(menu_id: int, session: AsyncSession = Depends(get_session)):
    menu_crud = CRUDClasses.MenuCRUD(session, redis_pool)
    return await menu_crud.get_menu(menu_id)


@app.patch("/api/v1/menus/{menu_id}", response_model=tables.MenuAll)
async def update_menu(menu_id: int, updated_menu: tables.MenuSchema, session: AsyncSession = Depends(get_session)):
    menu_crud = CRUDClasses.MenuCRUD(session, redis_pool)
    return await menu_crud.update_menu(menu_id, updated_menu)


@app.delete("/api/v1/menus/{menu_id}")
async def delete_menu(menu_id: int, session: AsyncSession = Depends(get_session)):
    menu_crud = CRUDClasses.MenuCRUD(session, redis_pool)
    return await menu_crud.delete_menu(menu_id)


@app.get("/api/v1/menus", response_model=List[tables.MenuAll])
async def get_all_menus(session: AsyncSession = Depends(get_session)):
    menu_crud = CRUDClasses.MenuCRUD(session, redis_pool)
    return await menu_crud.get_all_menus()


@app.post("/api/v1/menus/{menu_id}/submenus/", response_model=tables.SubmenuAll, status_code=201)
async def create_submenu(menu_id: int, submenu: tables.SubmenuSchema, session: AsyncSession = Depends(get_session)):
    submenu_crud = CRUDClasses.SubmenuCRUD(session, redis_pool)
    return await submenu_crud.create_submenu(submenu, menu_id)


@app.get("/api/v1/menus/{menu_id}/submenus/", response_model=List[tables.SubmenuAll])
async def get_all_submenus(menu_id: int, session: AsyncSession = Depends(get_session)):
    submenu_crud = CRUDClasses.SubmenuCRUD(session, redis_pool)
    return await submenu_crud.get_all_submenus(menu_id)


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}", response_model=tables.SubmenuAll)
async def read_submenu(submenu_id: int, session: AsyncSession = Depends(get_session)):
    submenu_crud = CRUDClasses.SubmenuCRUD(session, redis_pool)
    return await submenu_crud.get_submenu(submenu_id)


@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}", response_model=tables.SubmenuAll)
async def update_submenu(submenu_id: int, updated_submenu: tables.SubmenuSchema,
                         session: AsyncSession = Depends(get_session)):
    submenu_crud = CRUDClasses.SubmenuCRUD(session, redis_pool)
    return await submenu_crud.update_submenu(submenu_id, updated_submenu)


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
async def delete_submenu(submenu_id: int, session: AsyncSession = Depends(get_session)):
    submenu_crud = CRUDClasses.SubmenuCRUD(session, redis_pool)
    return await submenu_crud.delete_submenu(submenu_id)


@app.post("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/", response_model=tables.DishAll, status_code=201)
async def create_dish(submenu_id: int, dish: tables.DishSchema,
                      session: AsyncSession = Depends(get_session)):
    dish_crud = CRUDClasses.DishCRUD(session, redis_pool)
    return await dish_crud.create_dish(dish, submenu_id)


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/", response_model=List[tables.DishAll])
async def get_all_dishes(submenu_id: int, session: AsyncSession = Depends(get_session)):
    dish_crud = CRUDClasses.DishCRUD(session, redis_pool)
    return await dish_crud.get_all_dishes(submenu_id)


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=tables.DishAll)
async def read_dish(dish_id: int, session: AsyncSession = Depends(get_session)):
    dish_crud = CRUDClasses.DishCRUD(session, redis_pool)
    return await dish_crud.get_dish(dish_id)


@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=tables.DishAll)
async def update_dish(dish_id: int, updated_dish: tables.DishSchema, session: AsyncSession = Depends(get_session)):
    dish_crud = CRUDClasses.DishCRUD(session, redis_pool)
    return await dish_crud.update_dish(dish_id, updated_dish)


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def delete_dish(dish_id: int, session: AsyncSession = Depends(get_session)):
    dish_crud = CRUDClasses.DishCRUD(session, redis_pool)
    return await dish_crud.delete_dish(dish_id)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.on_event("startup")
async def startup_event():
    await tables.create_tables(engine)

    if test_check == "YES_I_WANT_TO_DELETE_MY_DATA":
        async with AsyncSession(engine) as session:
            yield session
            await session.execute(delete(tables.Dish))
            await session.execute(delete(tables.Submenu))
            await session.execute(delete(tables.Menu))
    import aioredis
    global redis_pool
    redis_url = "redis://localhost:6380"  # Replace with your actual Redis URL
    redis_pool = await aioredis.create_redis_pool(redis_url)
