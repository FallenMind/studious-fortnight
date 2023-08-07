import httpx


class MenuCRUD:
    def __init__(self, base_url):
        self.base_url = base_url

    async def create_menu(self, menu_data):
        async with httpx.AsyncClient() as client:
            return await client.post(self.base_url + '/api/v1/menus/', json=menu_data, follow_redirects=True)

    async def read_menu(self, menu_id):
        async with httpx.AsyncClient() as client:
            return await client.get(self.base_url + f'/api/v1/menus/{menu_id}', follow_redirects=True)

    async def get_all_menus(self):
        async with httpx.AsyncClient() as client:
            return await client.get(self.base_url + '/api/v1/menus/', follow_redirects=True)

    async def update_menu(self, menu_id, menu_data):
        async with httpx.AsyncClient() as client:
            return await client.patch(self.base_url + f'/api/v1/menus/{menu_id}', json=menu_data,
                                      follow_redirects=True)

    async def delete_menu(self, menu_id):
        async with httpx.AsyncClient() as client:
            return await client.delete(self.base_url + f'/api/v1/menus/{menu_id}', follow_redirects=True)


class SubmenuCRUD:
    def __init__(self, base_url):
        self.base_url = base_url

    async def create_submenu(self, menu_id, submenu_data):
        async with httpx.AsyncClient() as client:
            return await client.post(self.base_url + f'/api/v1/menus/{menu_id}/submenus', json=submenu_data,
                                     follow_redirects=True)

    async def read_submenu(self, menu_id, submenu_id):
        async with httpx.AsyncClient() as client:
            return await client.get(self.base_url + f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/',
                                    follow_redirects=True)

    async def get_all_submenus(self, menu_id):
        async with httpx.AsyncClient() as client:
            return await client.get(self.base_url + f'/api/v1/menus/{menu_id}/submenus/',
                                    follow_redirects=True)

    async def update_submenu(self, menu_id, submenu_id, submenu_data):
        async with httpx.AsyncClient() as client:
            return await client.patch(self.base_url + f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/',
                                      json=submenu_data,
                                      follow_redirects=True)

    async def delete_submenu(self, menu_id, submenu_id):
        async with httpx.AsyncClient() as client:
            return await client.delete(self.base_url + f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/',
                                       follow_redirects=True)


class DishCRUD:
    def __init__(self, base_url):
        self.base_url = base_url

    async def create_dish(self, menu_id, submenu_id, dish_data):
        async with httpx.AsyncClient() as client:
            return await client.post(self.base_url + f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
                                     json=dish_data,
                                     follow_redirects=True)

    async def read_dish(self, menu_id, submenu_id, dish_id):
        async with httpx.AsyncClient() as client:
            return await client.get(
                self.base_url + f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
                follow_redirects=True)

    async def get_all_dishes(self, menu_id, submenu_id):
        async with httpx.AsyncClient() as client:
            return await client.get(
                self.base_url + f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/',
                follow_redirects=True)

    async def update_dish(self, menu_id, submenu_id, dish_id, dish_data):
        async with httpx.AsyncClient() as client:
            return await client.patch(
                self.base_url + f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
                json=dish_data,
                follow_redirects=True)

    async def delete_dish(self, menu_id, submenu_id, dish_id):
        async with httpx.AsyncClient() as client:
            return await client.delete(
                self.base_url + f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
                follow_redirects=True)
