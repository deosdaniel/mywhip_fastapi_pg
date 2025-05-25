import pytest
from httpx import AsyncClient, ASGITransport

from .main import app


BASE_URL = '/api/v1/cars'

@pytest.mark.asyncio
async def test_get_all_cars():
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        response = await ac.get(f'{BASE_URL}/')
        data = response.json()