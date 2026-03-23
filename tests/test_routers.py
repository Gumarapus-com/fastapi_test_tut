class TestCreateNote:
    async def test_success(self, http):
        # async with http as http:
        response = await http.get('/')
        assert response.status_code == 200
        assert len(response.json()) == 0
