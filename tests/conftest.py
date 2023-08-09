import CRUD
import pytest_asyncio

base_url = 'http://host.docker.internal:8000'


@pytest_asyncio.fixture(autouse=True)
async def fixture_menu():
    menus = [
        {'title': 'Menu', 'description': 'New description'},
        {'title': 'Updated menu', 'description': 'Updated description'},
    ]
    return menus


@pytest_asyncio.fixture(autouse=True)
async def fixture_submenu():
    submenus = [
        {'title': 'Submenu', 'description': 'Description'},
        {'title': 'Updated submenu', 'description': 'Updated description'},
    ]
    return submenus


@pytest_asyncio.fixture(autouse=True)
async def fixture_dish():
    dishes = [
        {'title': 'Dish', 'description': 'Description', 'price': '12.50'},
        {'title': 'Updated dish', 'description': 'Updated description', 'price': '21.05'}
    ]
    return dishes


@pytest_asyncio.fixture
async def fixture_menu_id(fixture_menu):
    menu_data = fixture_menu
    response = await CRUD.MenuCRUD(base_url).create_menu(menu_data[0])
    assert response.status_code == 201
    assert fixture_menu[0]['title'] == response.json()['title']
    assert fixture_menu[0]['description'] == response.json()['description']
    return response.json()['id']


@pytest_asyncio.fixture
async def fixture_submenu_ids(fixture_menu_id, fixture_submenu):
    menu_id = fixture_menu_id
    response = await CRUD.SubmenuCRUD(base_url).create_submenu(menu_id, fixture_submenu[0])
    assert response.status_code == 201
    assert fixture_submenu[0]['title'] == response.json()['title']
    assert fixture_submenu[0]['description'] == response.json()['description']
    return menu_id, response.json()['id']


@pytest_asyncio.fixture
async def fixture_dish_ids(fixture_submenu_ids, fixture_dish):
    menu_id, submenu_id = fixture_submenu_ids
    response = await CRUD.DishCRUD(base_url).create_dish(menu_id, submenu_id, fixture_dish[0])
    assert response.status_code == 201
    assert fixture_dish[0]['title'] == response.json()['title']
    assert fixture_dish[0]['description'] == response.json()['description']
    assert fixture_dish[0]['price'] == response.json()['price']
    return menu_id, submenu_id, response.json()['id']
