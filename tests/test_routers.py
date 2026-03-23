class TestCreateNote:
    async def test_success(self, http):
        # async with http as http:
        response = await http.post('/', json={
            'name': 'New Note',
            'desc': 'New desc'
        })
        assert response.status_code == 201

        # Get
        response = await http.get(f'/{response.json()["id"]}')
        assert response.status_code == 200


class TestGetByID:
    async def test_empty(self, http):
        # async with http as http:
        response = await http.get('/100')
        assert response.status_code == 404

    async def test_success(self, http, a_note):
        # async with http as http:
        response = await http.get(f'/{a_note.id}')
        assert response.status_code == 200


class TestGetList:
    async def test_empty(self, http):
        # async with http as http:
        response = await http.get('/')
        assert response.status_code == 200
        assert len(response.json()) == 0

    async def test_success(self, http, a_note):
        # async with http as http:
        response = await http.get('/')
        assert response.status_code == 200
        assert len(response.json()) > 0


class TestUpdate:
    async def test_success(self, http, a_note):
        response = await http.put(f'/{a_note.id}', json={
            'name': 'New Name',
            'desc': 'New desc'
        })

        assert response.status_code == 202
        assert a_note.name != response.json()['name']
        assert a_note.desc != response.json()['desc']

    async def test_not_found(self, http, a_note):
        response = await http.put(f'/100', json={
            'name': 'New Name',
            'desc': 'New desc'
        })

        assert response.status_code == 404

