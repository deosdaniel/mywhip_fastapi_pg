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


# @pytest.mark.asyncio
# async def test_dir_get_all_makes(client, make_factory):
#    async with TestSession() as session:
#        await make_factory(session, "Toyota")
#        await make_factory(session, "Mitsubishi")
#        await make_factory(session, "Ford")
#        await make_factory(session, "Honda")
#
#    response = await client.get("/api/v1/directories/makes")
#    assert response.status == 200
#    result = response.json()["result"]
#    assert result["total_records"] == 4
