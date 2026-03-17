class TestCreateNote:
    async def test_success(self, http):
        async with http as http:
            response = await http.get()