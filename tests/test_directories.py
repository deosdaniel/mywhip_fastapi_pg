import uuid
import pytest
from sqlmodel import select
from src.db.core import get_session
from src.directories.models import MakesDirectory, ModelsDirectory


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

    response_negative_limit = await client.get("/api/v1/directories/makes?limit=-1")
    assert response_negative_limit.status_code == 422
    response_negative_page = await client.get("/api/v1/directories/makes?page=-1")
    assert response_negative_page.status_code == 422
    response_zero_page = await client.get("/api/v1/directories/makes?page=0")
    assert response_zero_page.status_code == 422
    response_too_far_page = await client.get("/api/v1/directories/makes?page=100500")
    assert response_too_far_page.status_code == 200
    data_far_page = response_too_far_page.json()
    assert len(data_far_page["result"]["content"]) == 0
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

    response_negative_limit = await client.get("/api/v1/directories/models?limit=-1")
    assert response_negative_limit.status_code == 422
    response_zero_limit = await client.get("/api/v1/directories/models?limit=0")
    assert response_zero_limit.status_code == 422
    response_negative_page = await client.get("/api/v1/directories/models?page=-1")
    assert response_negative_page.status_code == 422
    response_zero_page = await client.get("/api/v1/directories/models?page=0")
    assert response_zero_page.status_code == 422
    response_too_far_page = await client.get("/api/v1/directories/models?page=100500")
    assert response_too_far_page.status_code == 200
    data_far_page = response_too_far_page.json()
    assert len(data_far_page["result"]["content"]) == 0
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
async def test_get_models_by_make_success(client):
    prep_response = await client.get("/api/v1/directories/makes")
    assert prep_response.status_code == 200
    prep_data = prep_response.json()["result"]
    test_make_uid = prep_data["content"][0]["uid"]

    response = await client.get(f"/api/v1/directories/makes/{test_make_uid}/models")
    assert response.status_code == 200
    data = response.json()["result"]
    assert len(data["content"]) > 0


@pytest.mark.asyncio
async def test_get_models_by_make_nonexistent_make_uid(client):
    nonexistent_uid = uuid.uuid4()
    response = await client.get(f"/api/v1/directories/makes/{nonexistent_uid}/models")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_models_by_make_invalid_make_uid(client):
    response = await client.get(f"/api/v1/directories/makes/123/models")
    assert response.status_code == 422
