import pytest
from conftest import base_url
from CRUD import DishCRUD, MenuCRUD


@pytest.mark.asyncio
async def test_dish_read(fixture_dish_ids, fixture_dish):
    menu_id, submenu_id, dish_id = fixture_dish_ids
    response = await DishCRUD(base_url).read_dish(menu_id, submenu_id, dish_id)
    assert response.status_code == 200
    assert fixture_dish[0]['title'] == response.json()['title']
    assert fixture_dish[0]['description'] == response.json()['description']
    assert fixture_dish[0]['price'] == response.json()['price']
    response = await MenuCRUD(base_url).delete_menu(menu_id)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_all_dishes(fixture_dish_ids):
    menu_id, submenu_id, _ = fixture_dish_ids
    response = await DishCRUD(base_url).get_all_dishes(menu_id, submenu_id)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    response = await MenuCRUD(base_url).delete_menu(menu_id)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_dish_update(fixture_dish_ids, fixture_dish):
    menu_id, submenu_id, dish_id = fixture_dish_ids
    response = await DishCRUD(base_url).update_dish(menu_id, submenu_id, dish_id, fixture_dish[1])
    assert response.status_code == 200
    assert fixture_dish[1]['title'] == response.json()['title']
    assert fixture_dish[1]['description'] == response.json()['description']
    assert fixture_dish[1]['price'] == response.json()['price']
    response = await MenuCRUD(base_url).delete_menu(menu_id)
    assert response.status_code == 200
