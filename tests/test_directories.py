import pytest
from sqlmodel import select

from src.db.core import get_session
from src.directories.models import MakesDirectory, ModelsDirectory
from tests.conftest import TestSession


@pytest.mark.asyncio
async def test_directories_loaded(test_session):
    async for session in get_session():
        makes = await session.exec(select(MakesDirectory))
        makes = makes.all()
        assert makes, "Таблица makesdir пустая"

        models = await session.exec(
            select(ModelsDirectory).where(ModelsDirectory.make_uid == makes[0].uid)
        )
        models = models.all()
        assert models, "Для первой марки нет моделей"


@pytest.mark.asyncio
async def test_get_all_makes(client):
    response = await client.get("/api/v1/directories/makes")
    assert response.status_code == 200
    data = response.json()["result"]
    assert "content" in data
    assert isinstance(data["content"], list)
    assert len(data["content"]) > 0
    # Pagination
    response_2 = await client.get("/api/v1/directories/makes?page=1&limit=1")
    data_2 = response_2.json()
    assert len(data_2["result"]["content"]) == 1
    # Order_by
    response_3 = await client.get(
        "/api/v1/directories/makes?page=1&limit=10&order_by=desc"
    )
    data_3 = response_3.json()
    assert (
        data_3["result"]["content"][0]["make"] > data_3["result"]["content"][-1]["make"]
    )


@pytest.mark.asyncio
async def test_get_all_models(client):
    response = await client.get("/api/v1/directories/models")
    assert response.status_code == 200
    data = response.json()["result"]
    assert "content" in data
    assert isinstance(data["content"], list)
    assert len(data["content"]) > 0
    # Pagination
    response_2 = await client.get("/api/v1/directories/models?page=1&limit=1")
    data_2 = response_2.json()
    assert len(data_2["result"]["content"]) == 1
    # Order_by
    response_3 = await client.get(
        "/api/v1/directories/models?page=1&limit=10&order_by=desc"
    )
    data_3 = response_3.json()
    assert (
        data_3["result"]["content"][0]["model"]
        > data_3["result"]["content"][-1]["model"]
    )


@pytest.mark.asyncio
async def test_get_models_by_make(client):
    response = await client.get("/api/v1/directories/makes/{make_uid}/models")
