import pytest

from tests.conftest import TestSession


@pytest.mark.asyncio
async def test_dir_get_all_makes(client, make_factory):
    async with TestSession() as session:
        await make_factory(session, "Toyota")
        await make_factory(session, "Mitsubishi")
        await make_factory(session, "Ford")
        await make_factory(session, "Honda")

    response = await client.get("/api/v1/directories/makes")
    assert response.status == 200
    result = response.json()["result"]
    assert result["total_records"] == 4
