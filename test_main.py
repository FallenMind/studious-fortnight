import pytest
from typing import List
import httpx

# Define the base URL of the unknown server (Replace with the actual server URL)
base_url = "http://localhost:8000"


@pytest.mark.skip
@pytest.mark.asyncio
async def read_menu(menu_id):
    if menu_id is 999:
        # No pages available, assert 404 status code for menu not found
        async with httpx.AsyncClient() as client:
            response = await client.get(base_url + "/api/v1/menus/999", follow_redirects=True)  # Use an invalid menu_id
            assert response.status_code == 404
            data = response.json()
            assert "detail" in data
            assert data["detail"] == "menu not found"
    else:
        async with httpx.AsyncClient() as client:
            response = await client.get(base_url + f"/api/v1/menus/{menu_id}", follow_redirects=True)
            assert response.status_code == 200
            data = response.json()
            assert data["title"] == "Menu 1"
            assert data["description"] == "Description 1"


@pytest.mark.skip
@pytest.mark.asyncio
async def get_all_menus():
    async with httpx.AsyncClient() as client:
        response = await client.get(base_url + "/api/v1/menus", follow_redirects=True)
        assert response.status_code == 200
        data = response.json()
        if len(data) == 0:
            assert data == []
        else:
            assert isinstance(data, List)

@pytest.mark.skip
@pytest.mark.asyncio
async def create_menu():
    async with httpx.AsyncClient() as client:
        menu_data = {"title": "Menu 1", "description": "Description 1"}
        response = await client.post(base_url + "/api/v1/menus", json=menu_data, follow_redirects=True)
        assert response.status_code == 201
        data = response.json()
        return data["id"]


@pytest.mark.skip
@pytest.mark.asyncio
async def update_menu(menu_id):
    async with httpx.AsyncClient() as client:
        if menu_id is 999:
            # No pages available, assert 404 status code for menu not found
            menu_data = {"title": "Updated Menu", "description": "Updated Description"}
            response = await client.patch(base_url + f"/api/v1/menus/999", json=menu_data,
                                          follow_redirects=True)  # Use an invalid menu_id
            assert response.status_code == 404
            data = response.json()
            assert "detail" in data
            assert data["detail"] == "menu not found"
        else:
            menu_data = {"title": "Updated Menu", "description": "Updated Description"}
            response = await client.patch(base_url + f"/api/v1/menus/{menu_id}", json=menu_data, follow_redirects=True)
            assert response.status_code == 200
            data = response.json()
            assert data["title"] == menu_data["title"]
            assert data["description"] == menu_data["description"]


@pytest.mark.skip
@pytest.mark.asyncio
async def delete_menu(menu_id):
    async with httpx.AsyncClient() as client:
        if menu_id is 999:
            # No pages available, assert 404 status code for menu not found
            response = await client.delete(base_url + f"/api/v1/menus/999",
                                           follow_redirects=True)  # Use an invalid menu_id
            assert response.status_code == 404
            data = response.json()
            assert "detail" in data
            assert data["detail"] == "menu not found"
        else:
            response = await client.delete(base_url + f"/api/v1/menus/{menu_id}", follow_redirects=True)
            assert response.status_code == 200
            data = response.json()
            assert "message" in data
            assert data["message"] == "Menu deleted successfully."


@pytest.mark.skip
@pytest.mark.asyncio
async def read_submenu(menu_id, submenu_id):
    if submenu_id is 999:
        # No pages available, assert 404 status code for menu not found
        async with httpx.AsyncClient() as client:
            response = await client.get(base_url + f"/api/v1/menus/{menu_id}/submenus/999/",
                                        follow_redirects=True)  # Use an invalid menu_id
            assert response.status_code == 404
            data = response.json()
            assert "detail" in data
            assert data["detail"] == "menu not found"
    else:
        async with httpx.AsyncClient() as client:
            response = await client.get(base_url + f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/", follow_redirects=True)
            assert response.status_code == 200
            data = response.json()
            assert data["title"] == "Menu 1"
            assert data["description"] == "Description 1"


@pytest.mark.skip
@pytest.mark.asyncio
async def get_all_submenus(menu_id):
    async with httpx.AsyncClient() as client:
        response = await client.get(base_url + f"/api/v1/menus/{menu_id}/", follow_redirects=True)
        assert response.status_code == 200
        data = response.json()
        if len(data) == 0:
            assert data == []
        else:
            assert isinstance(data, List)


@pytest.mark.skip
@pytest.mark.asyncio
async def create_submenu(menu_id):
    if menu_id is 999:
        async with httpx.AsyncClient() as client:
            submenu_data = {"title": "Sub Menu", "description": "Description"}
            response = await client.post(base_url + f"/api/v1/menus/999/submenus", json=submenu_data,
                                         follow_redirects=True)  # Use an invalid menu_id
            assert response.status_code == 404
            data = response.json()
            assert "detail" in data
            assert data["detail"] == "menu not found"
    else:
        async with httpx.AsyncClient() as client:
            submenu_data = {"title": "Sub Menu", "description": "Description"}
            response = await client.post(base_url + f"/api/v1/menus/{menu_id}/submenus", json=submenu_data,
                                         follow_redirects=True)
            assert response.status_code == 201
            data = response.json()
            return data["id"]


@pytest.mark.skip
@pytest.mark.asyncio
async def update_submenu(menu_id, submenu_id):
    async with httpx.AsyncClient() as client:
        if submenu_id is 999:
            # No pages available, assert 404 status code for menu not found
            submenu_data = {"title": "My submenu 1", "description": "My submenu description 1"}
            response = await client.patch(base_url + f"/api/v1/menus/999/submenus/999/", json=submenu_data,
                                          follow_redirects=True)  # Use an invalid menu_id
            assert response.status_code == 404
            data = response.json()
            assert "detail" in data
            assert data["detail"] == 'Submenu not found.'
        else:
            submenu_data = {"title": "Sub Menu", "description": "Description"}
            response = await client.patch(base_url + f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/", json=submenu_data,
                                          follow_redirects=True)
            assert response.status_code == 200
            data = response.json()
            assert data["title"] == submenu_data["title"]
            assert data["description"] == submenu_data["description"]


@pytest.mark.skip
@pytest.mark.asyncio
async def delete_submenu(menu_id, submenu_id):
    async with httpx.AsyncClient() as client:
        if submenu_id is 999:
            # No pages available, assert 404 status code for menu not found
            response = await client.delete(base_url + f"/api/v1/menus/999/submenus/999/",
                                           follow_redirects=True)  # Use an invalid menu_id
            assert response.status_code == 404
            data = response.json()
            assert "detail" in data
            assert data["detail"] == 'Submenu not found.'
        else:
            response = await client.delete(base_url + f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/", follow_redirects=True)
            assert response.status_code == 200
            data = response.json()
            assert "message" in data
            assert data["message"] == "Submenu deleted successfully."


@pytest.mark.skip
@pytest.mark.asyncio
async def read_dish(menu_id, submenu_id, dish_id):
    if dish_id is 999:
        # No pages available, assert 404 status code for menu not found
        async with httpx.AsyncClient() as client:
            response = await client.get(base_url + f"/api/v1/menus/999/submenus/999/dishes/999/",
                                        follow_redirects=True)  # Use an invalid menu_id
            assert response.status_code == 404
            data = response.json()
            assert "detail" in data
            assert data["detail"] == "dish not found"
    else:
        async with httpx.AsyncClient() as client:
            response = await client.get(base_url + f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", follow_redirects=True)
            assert response.status_code == 200
            data = response.json()
            assert data["title"] == "Di sh"
            assert data["description"] == 'Description'


@pytest.mark.skip
@pytest.mark.asyncio
async def get_all_dishes(menu_id, submenu_id):
    async with httpx.AsyncClient() as client:
        response = await client.get(base_url + f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", follow_redirects=True)
        assert response.status_code == 200
        data = response.json()
        if len(data) == 0:
            assert data == []
        else:
            assert isinstance(data, List)


@pytest.mark.skip
@pytest.mark.asyncio
async def create_dish(menu_id, submenu_id):
    if submenu_id is 999:
        async with httpx.AsyncClient() as client:
            dish_data = {"title": "Di sh", "description": "Description", "price": "12.50"}
            response = await client.post(base_url + f"/api/v1/menus/999/submenus/999/dishes", json=dish_data,
                                         follow_redirects=True)  # Use an invalid menu_id
            assert response.status_code == 404
            data = response.json()
            assert "detail" in data
            assert data["detail"] == "menu not found"
    else:
        async with httpx.AsyncClient() as client:
            dish_data = {"title": "Di sh", "description": "Description", "price": "12.50"}
            response = await client.post(base_url + f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", json=dish_data,
                                         follow_redirects=True)
            assert response.status_code == 201
            data = response.json()
            return data["id"]


@pytest.mark.skip
@pytest.mark.asyncio
async def update_dish(menu_id, submenu_id, dish_id):
    async with httpx.AsyncClient() as client:
        if menu_id is 999:
            # No pages available, assert 404 status code for menu not found
            dish_data = {"title": "Di sh", "description": "Description", "price": "12.50"}
            response = await client.patch(base_url + f"/api/v1/menus/999/submenus/999/dishes/999", json=dish_data,
                                          follow_redirects=True)  # Use an invalid menu_id
            assert response.status_code == 404
            data = response.json()
            assert "detail" in data
            assert data["detail"] == 'dish not found'
        else:
            dish_data = {"title": "Di sh", "description": "Description", "price": "12.50"}
            response = await client.patch(base_url + f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", json=dish_data,
                                          follow_redirects=True)
            assert response.status_code == 200
            data = response.json()
            assert data["title"] == dish_data["title"]
            assert data["description"] == dish_data["description"]


@pytest.mark.skip
@pytest.mark.asyncio
async def delete_dish(menu_id, submenu_id, dish_id):
    async with httpx.AsyncClient() as client:
        if dish_id is 999:
            # No pages available, assert 404 status code for menu not found
            response = await client.delete(base_url + f"/api/v1/menus/999/submenus/999/dishes/999",
                                           follow_redirects=True)  # Use an invalid menu_id
            assert response.status_code == 404
            data = response.json()
            assert "detail" in data
            assert data["detail"] == 'dish not found'
        else:
            response = await client.delete(base_url + f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", follow_redirects=True)
            assert response.status_code == 200
            data = response.json()
            assert "message" in data
            assert data["message"] == 'Dish deleted successfully.'


# Run the tests
@pytest.mark.skip
@pytest.mark.asyncio
async def test_unit_menus_for_404():
    menu_id = 999
    await update_menu(menu_id)
    await delete_menu(menu_id)
    await get_all_menus()
    await read_menu(menu_id)

@pytest.mark.skip
@pytest.mark.asyncio
async def test_unit_menus_for_200():
    menu_id = await create_menu()
    await get_all_menus()
    await read_menu(menu_id)
    await update_menu(menu_id)
    await delete_menu(menu_id)


@pytest.mark.asyncio
async def test_unit_submenus_for_404():
    submenu_id = 999
    menu_id = 999
    await update_submenu(menu_id, submenu_id)
    await delete_submenu(menu_id, submenu_id)
    await get_all_submenus(menu_id)
    await read_submenu(menu_id, submenu_id)


@pytest.mark.asyncio
async def test_unit_submenus_for_200():
    menu_id = await create_menu()
    submenu_id = await create_submenu(menu_id)
    await get_all_submenus(menu_id)
    await read_submenu(menu_id, submenu_id)
    await update_submenu(menu_id, submenu_id)
    await delete_submenu(menu_id, submenu_id)
    await delete_menu(menu_id)


@pytest.mark.asyncio
async def test_unit_dishes_for_404():
    submenu_id = 999
    menu_id = 999
    dish_id = 999
    await update_dish(menu_id, submenu_id, dish_id)
    await delete_dish(menu_id, submenu_id, dish_id)
    await get_all_dishes(menu_id, submenu_id)
    await read_dish(menu_id, submenu_id, dish_id)


@pytest.mark.asyncio
async def test_unit_dishes_for_200():
    menu_id = await create_menu()
    submenu_id = await create_submenu(menu_id)
    dish_id = await create_dish(menu_id, submenu_id)
    await get_all_dishes(menu_id, submenu_id)
    await read_dish(menu_id, submenu_id, dish_id)
    await update_dish(menu_id, submenu_id, dish_id)
    await delete_dish(menu_id, submenu_id, dish_id)
    await delete_menu(menu_id)
