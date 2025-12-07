import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from app.interfaces.api.v1.routes import router as v1_router
from app.interfaces.api.dependencies import get_db_session


@pytest.fixture
async def api_client(test_db_session):
    """FastAPI test client with in-memory DB session injected."""

    app = FastAPI()
    app.include_router(v1_router)

    async def override_get_db_session():
        yield test_db_session

    app.dependency_overrides[get_db_session] = override_get_db_session

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_create_and_delete_mechanic(api_client):
    payload = {"name": "Jump", "description": "player jump", "year": 1978}

    r_create = await api_client.post("/api/v1/mechanics/", json=payload)
    assert r_create.status_code == 201
    mech = r_create.json()
    assert mech["name"] == "Jump"

    r_list = await api_client.get("/api/v1/mechanics/")
    assert r_list.status_code == 200
    assert any(m["id"] == mech["id"] for m in r_list.json())

    r_del = await api_client.delete(f"/api/v1/mechanics/{mech['id']}")
    assert r_del.status_code == 204

    r_after = await api_client.get("/api/v1/mechanics/")
    assert r_after.status_code == 200
    assert all(m["id"] != mech["id"] for m in r_after.json())


@pytest.mark.asyncio
async def test_create_link_between_mechanics(api_client):
    r1 = await api_client.post(
        "/api/v1/mechanics/",
        json={"name": "Jump", "description": "player jump", "year": 1978},
    )
    r2 = await api_client.post(
        "/api/v1/mechanics/",
        json={"name": "Double Jump", "description": "double", "year": 1990},
    )
    assert r1.status_code == 201 and r2.status_code == 201
    m1, m2 = r1.json(), r2.json()

    r_link = await api_client.post(
        "/api/v1/mechanics/links",
        json={"from_id": m1["id"], "to_id": m2["id"], "type": "evolution"},
    )
    assert r_link.status_code == 201
    link = r_link.json()
    assert link["from_id"] == m1["id"] and link["to_id"] == m2["id"]

    r_links = await api_client.get("/api/v1/mechanics/links")
    assert r_links.status_code == 200
    data = r_links.json()
    assert len(data) == 1
    assert data[0]["type"] == "evolution"


@pytest.mark.asyncio
async def test_links_removed_when_mechanic_deleted(api_client):
    r1 = await api_client.post(
        "/api/v1/mechanics/",
        json={"name": "A", "description": "", "year": 2000},
    )
    r2 = await api_client.post(
        "/api/v1/mechanics/",
        json={"name": "B", "description": "", "year": 2001},
    )
    m1, m2 = r1.json(), r2.json()

    await api_client.post(
        "/api/v1/mechanics/links",
        json={"from_id": m1["id"], "to_id": m2["id"], "type": "evolution"},
    )

    r_links_before = await api_client.get("/api/v1/mechanics/links")
    assert r_links_before.status_code == 200
    assert len(r_links_before.json()) == 1

    r_del = await api_client.delete(f"/api/v1/mechanics/{m1['id']}")
    assert r_del.status_code == 204

    r_links_after = await api_client.get("/api/v1/mechanics/links")
    assert r_links_after.status_code == 200
    assert r_links_after.json() == []