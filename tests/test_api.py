async def test_has_openapi_json(api_client):
    response = await api_client.get("/openapi.json")
    assert response.status_code == 200


async def test_failure():
    assert False
