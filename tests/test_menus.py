import pytest
from conftest import base_url
from CRUD import MenuCRUD


@pytest.mark.asyncio
async def test_menu_read(fixture_menu_id, fixture_menu):
    response = await MenuCRUD(base_url).read_menu(fixture_menu_id)
    assert response.status_code == 200
    assert fixture_menu[0]['title'] == response.json()['title']
    assert fixture_menu[0]['description'] == response.json()['description']
    response = await MenuCRUD(base_url).delete_menu(fixture_menu_id)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_all_menus(fixture_menu_id):
    _ = fixture_menu_id
    response = await MenuCRUD(base_url).get_all_menus()
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    response = await MenuCRUD(base_url).delete_menu(_)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_menu_update(fixture_menu_id, fixture_menu):
    response = await MenuCRUD(base_url).update_menu(fixture_menu_id, fixture_menu[1])
    assert response.status_code == 200
    assert fixture_menu[1]['title'] == response.json()['title']
    assert fixture_menu[1]['description'] == response.json()['description']
    response = await MenuCRUD(base_url).delete_menu(fixture_menu_id)
    assert response.status_code == 200
