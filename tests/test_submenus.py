import pytest
from conftest import base_url
from CRUD import MenuCRUD, SubmenuCRUD


@pytest.mark.asyncio
async def test_submenu_read(fixture_submenu_ids, fixture_submenu):
    menu_id, submenu_id = fixture_submenu_ids
    response = await SubmenuCRUD(base_url).read_submenu(menu_id, submenu_id)
    assert response.status_code == 200
    assert fixture_submenu[0]['title'] == response.json()['title']
    assert fixture_submenu[0]['description'] == response.json()['description']
    response = await MenuCRUD(base_url).delete_menu(menu_id)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_all_submenus(fixture_submenu_ids):
    menu_id, _ = fixture_submenu_ids
    response = await SubmenuCRUD(base_url).get_all_submenus(menu_id)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    response = await MenuCRUD(base_url).delete_menu(menu_id)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_submenu_update(fixture_submenu_ids, fixture_submenu):
    menu_id, submenu_id = fixture_submenu_ids
    response = await SubmenuCRUD(base_url).update_submenu(menu_id, submenu_id, fixture_submenu[1])
    assert response.status_code == 200
    assert fixture_submenu[1]['title'] == response.json()['title']
    assert fixture_submenu[1]['description'] == response.json()['description']
    response = await MenuCRUD(base_url).delete_menu(menu_id)
    assert response.status_code == 200
