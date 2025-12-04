import pytest

async def test_create_and_get_tree(client):
    # create two mechanics and a link
    r1 = await client.post("/api/v1/mechanics", json={"name":"Jump", "description":"player jump", "year":1978})
    assert r1.status_code == 201
    m1 = r1.json()

    r2 = await client.post("/api/v1/mechanics", json={"name":"Double Jump", "description":"player double jump", "year":1990})
    assert r2.status_code == 201
    m2 = r2.json()

    rlink = await client.post("/api/v1/links", json={"from_id": m1["id"], "to_id": m2["id"], "type":"evolution"})
    assert rlink.status_code == 201

    rtree = await client.get(f"/api/v1/mechanics/{m1['id']}/tree")
    assert rtree.status_code == 200
    payload = rtree.json()
    assert payload["root"]["id"] == m1["id"]
    assert len(payload["root"]["children"]) == 1