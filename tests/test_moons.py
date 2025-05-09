import pytest

def test_create_and_list_moons(client, two_saved_planets):
    # 1) No moons yet
    resp = client.get("/planets/1/moons")
    assert resp.status_code == 200
    assert resp.get_json() == {"moons": []}

    # 2) Create one
    new_moon = {"name": "Luna", "size": 0.27, "description": "Earth’s moon"}
    post = client.post("/planets/1/moons", json=new_moon)
    assert post.status_code == 201
    moon_data = post.get_json()["moon"]
    assert moon_data["planet_id"] == 1
    assert moon_data["name"] == "Luna"

    # 3) Now list again
    resp2 = client.get("/planets/1/moons")
    moons = resp2.get_json()["moons"]
    assert len(moons) == 1
    assert moons[0]["name"] == "Luna"
    
def test_get_moons_empty(client, two_saved_planets):
    resp = client.get("/planets/1/moons")
    assert resp.status_code == 200
    assert resp.get_json() == {"moons": []}

def test_create_moon_and_list(client, two_saved_planets):
    # create a moon
    new_moon = {"name": "Luna", "size": 0.27}
    post = client.post("/planets/1/moons", json=new_moon)
    assert post.status_code == 201
    moon = post.get_json()["moon"]
    assert moon["name"] == "Luna"
    # list again
    get = client.get("/planets/1/moons")
    assert len(get.get_json()["moons"]) == 1