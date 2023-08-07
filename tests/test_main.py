import pytest
from CRUD import DishCRUD, MenuCRUD, SubmenuCRUD

# Define the base URL of the unknown server (Replace with the actual server URL)
base_url = 'http://host.docker.internal:8000'


# Run the tests
@pytest.mark.asyncio
async def test_unit_menus_for_404():
    menu_crud = MenuCRUD(base_url)
    menu_id = 999
    new_data = {'title': 'Menu', 'description': 'Description'}

    response = await menu_crud.update_menu(menu_id, new_data)
    code = response.status_code
    response_data = response.json()
    assert code == 404
    assert 'detail' in response_data
    assert response_data['detail'] == 'menu not found'

    response = await menu_crud.delete_menu(menu_id)
    code = response.status_code
    response_data = response.json()
    assert code == 404
    assert 'detail' in response_data
    assert response_data['detail'] == 'menu not found'

    response = await menu_crud.get_all_menus()
    code = response.status_code
    response_data = response.json()
    assert code == 200
    assert response_data == []

    response = await menu_crud.read_menu(menu_id)
    code = response.status_code
    response_data = response.json()
    assert code == 404
    assert 'detail' in response_data
    assert response_data['detail'] == 'menu not found'


@pytest.mark.asyncio
async def test_unit_menus_for_200():
    menu_crud = MenuCRUD(base_url)
    new_data = {'title': 'Updated Menu', 'description': 'Updated Description'}
    data = {'title': 'Menu', 'description': 'Description'}

    response = await menu_crud.create_menu(data)
    code = response.status_code
    assert code == 201
    response_data = response.json()
    menu_id = response_data['id']

    response = await menu_crud.get_all_menus()
    code = response.status_code
    response_data = response.json()
    assert code == 200
    assert isinstance(response_data, list)

    response = await menu_crud.read_menu(menu_id)
    code = response.status_code
    response_data = response.json()
    assert code == 200
    assert response_data['title'] == 'Menu'
    assert response_data['description'] == 'Description'

    response = await menu_crud.update_menu(menu_id, new_data)
    code = response.status_code
    response_data = response.json()
    assert code == 200
    assert response_data['title'] == 'Updated Menu'
    assert response_data['description'] == 'Updated Description'

    response = await menu_crud.delete_menu(menu_id)
    code = response.status_code
    assert code == 200

# Test cases for SubmenuCRUD


@pytest.mark.asyncio
async def test_unit_submenus_for_404():
    submenu_crud = SubmenuCRUD(base_url)
    menu_id = 999
    submenu_id = 999
    new_data = {'title': 'Updated SubMenu', 'description': 'Updated Description'}

    response = await submenu_crud.update_submenu(menu_id, submenu_id, new_data)
    code = response.status_code
    response_data = response.json()
    assert code == 404
    assert 'detail' in response_data
    assert response_data['detail'] == 'Submenu not found.'

    response = await submenu_crud.delete_submenu(menu_id, submenu_id)
    code = response.status_code
    response_data = response.json()
    assert code == 404
    assert 'detail' in response_data
    assert response_data['detail'] == 'Submenu not found.'

    response = await submenu_crud.get_all_submenus(menu_id)
    code = response.status_code
    response_data = response.json()
    assert code == 200
    assert response_data == []

    response = await submenu_crud.read_submenu(menu_id, submenu_id)
    code = response.status_code
    response_data = response.json()
    assert code == 404
    assert 'detail' in response_data
    assert response_data['detail'] == 'submenu not found'


@pytest.mark.asyncio
async def test_unit_submenus_for_200():
    menu_crud = MenuCRUD(base_url)
    submenu_crud = SubmenuCRUD(base_url)
    new_data = {'title': 'Updated SubMenu', 'description': 'Updated Description'}
    data = {'title': 'SubMenu', 'description': 'Description'}

    response = await menu_crud.create_menu({'title': '1', 'description': '1'})
    code = response.status_code
    response_data = response.json()
    assert code == 201
    menu_id = response_data['id']
    response = await submenu_crud.create_submenu(menu_id, data)
    code = response.status_code
    assert code == 201
    response_data = response.json()
    submenu_id = response_data['id']

    response = await submenu_crud.get_all_submenus(menu_id)
    code = response.status_code
    response_data = response.json()
    assert code == 200
    assert isinstance(response_data, list)

    response = await submenu_crud.read_submenu(menu_id, submenu_id)
    code = response.status_code
    response_data = response.json()
    assert code == 200
    assert response_data['title'] == data['title']
    assert response_data['description'] == data['description']

    response = await submenu_crud.update_submenu(menu_id, submenu_id, new_data)
    code = response.status_code
    response_data = response.json()
    assert code == 200
    assert response_data['title'] == new_data['title']
    assert response_data['description'] == new_data['description']

    response = await submenu_crud.delete_submenu(menu_id, submenu_id)
    code = response.status_code
    response_data = response.json()
    assert code == 200
    assert 'message' in response_data
    assert response_data['message'] == 'Submenu deleted successfully.'

    response = await menu_crud.delete_menu(menu_id)
    code = response.status_code
    assert code == 200


# Test cases for DishCRUD
@pytest.mark.asyncio
async def test_unit_dishes_for_404():
    menu_id = 999
    submenu_id = 999
    dish_id = 999
    dish_crud = DishCRUD(base_url)
    new_data = {'title': 'New Di sh', 'description': 'New Description', 'price': '24.50'}

    response = await dish_crud.update_dish(menu_id, submenu_id, dish_id, new_data)
    code = response.status_code
    response_data = response.json()
    assert code == 404
    assert 'detail' in response_data
    assert response_data['detail'] == 'dish not found'

    response = await dish_crud.delete_dish(menu_id, submenu_id, dish_id)
    code = response.status_code
    response_data = response.json()
    assert code == 404
    assert 'detail' in response_data
    assert response_data['detail'] == 'dish not found'

    response = await dish_crud.get_all_dishes(menu_id, submenu_id)
    code = response.status_code
    response_data = response.json()
    assert code == 200
    assert response_data == []

    response = await dish_crud.read_dish(menu_id, submenu_id, dish_id)
    code = response.status_code
    response_data = response.json()
    assert code == 404
    assert 'detail' in response_data
    assert response_data['detail'] == 'dish not found'


@pytest.mark.asyncio
async def test_unit_dishes_for_200():
    menu_crud = MenuCRUD(base_url)
    submenu_crud = SubmenuCRUD(base_url)
    dish_crud = DishCRUD(base_url)
    new_data = {'title': 'New Di sh', 'description': 'New Description', 'price': '24.50'}

    response = await menu_crud.create_menu({'title': '1', 'description': '1'})
    code = response.status_code
    assert code == 201
    response_data = response.json()
    menu_id = response_data['id']
    response = await submenu_crud.create_submenu(menu_id, {'title': 'SubMenu', 'description': 'Description'})
    code = response.status_code
    assert code == 201
    response_data = response.json()
    submenu_id = response_data['id']
    response = await dish_crud.create_dish(menu_id, submenu_id,
                                           {'title': 'Di sh', 'description': 'Description',
                                            'price': '12.50'})
    code = response.status_code
    assert code == 201
    response_data = response.json()
    dish_id = response_data['id']

    response = await dish_crud.get_all_dishes(menu_id, submenu_id)
    code = response.status_code
    response_data = response.json()
    assert code == 200
    assert isinstance(response_data, list)

    response = await dish_crud.read_dish(menu_id, submenu_id, dish_id)
    code = response.status_code
    response_data = response.json()
    assert code == 200
    assert response_data['title'] == 'Di sh'
    assert response_data['description'] == 'Description'
    assert response_data['price'] == '12.50'

    response = await dish_crud.update_dish(menu_id, submenu_id, dish_id, new_data)
    code = response.status_code
    response_data = response.json()
    assert code == 200
    assert response_data['title'] == 'New Di sh'
    assert response_data['description'] == 'New Description'
    assert response_data['price'] == '24.50'

    response = await dish_crud.delete_dish(menu_id, submenu_id, dish_id)
    code = response.status_code
    response_data = response.json()
    assert code == 200
    assert 'message' in response_data
    assert response_data['message'] == 'Dish deleted successfully.'

    response = await submenu_crud.delete_submenu(menu_id, submenu_id)
    code = response.status_code
    assert code == 200

    response = await menu_crud.delete_menu(menu_id)
    code = response.status_code
    assert code == 200
