from httpx import AsyncClient
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import Entitlement
from tests.utils import assert_json_contains_model


async def test_can_create_entitlements(api_client: AsyncClient, db_session: AsyncSession):
    response = await api_client.post(
        "/entitlements/",
        json={
            "sponsorName": "AWS",
            "sponsorExternalId": "EXTERNAL_ID_987123",
            "sponsorContainerId": "SPONSOR_CONTAINER_ID_1234",
        },
    )

    assert response.status_code == 201
    data = response.json()

    assert data["id"] is not None
    assert data["activatedAt"] is None
    assert data["sponsorName"] == "AWS"
    assert data["sponsorExternalId"] == "EXTERNAL_ID_987123"
    assert data["sponsorContainerId"] == "SPONSOR_CONTAINER_ID_1234"

    result = await db_session.exec(select(Entitlement).where(Entitlement.id == data["id"]))
    assert result.one_or_none() is not None


async def test_get_all_entitlements_empty_db(api_client: AsyncClient):
    response = await api_client.get("/entitlements/")

    assert response.status_code == 200
    assert response.json()["total"] == 0
    assert response.json()["items"] == []


async def test_get_all_entitlements_single_page(entitlement_aws, entitlement_gcp, api_client: AsyncClient):
    response = await api_client.get("/entitlements/")

    assert response.status_code == 200
    data = response.json()

    assert data["total"] == 2
    assert len(data["items"]) == data["total"]

    assert_json_contains_model(data, entitlement_aws)
    assert_json_contains_model(data, entitlement_gcp)


async def test_can_update_entitlements(entitlement_aws, api_client):
    assert entitlement_aws.sponsor_name == "AWS"

    update_response = await api_client.patch(
        f"/entitlements/{entitlement_aws.id}",
        json={"sponsorName": "GCP"},
    )

    assert update_response.status_code == 200
    update_data = update_response.json()

    assert update_data["sponsorName"] == "GCP"

    get_response = await api_client.get(f"/entitlements/{entitlement_aws.id}")
    assert get_response.json()["sponsorName"] == "GCP"


async def test_get_all_entitlements_empty_db(api_client: AsyncClient):
    response = await api_client.get("/entitlements/")

    assert response.status_code == 200
    assert response.json()["total"] == 0
    assert response.json()["items"] == []


async def test_get_all_entitlements_single_page(entitlement_aws, entitlement_gcp, api_client: AsyncClient):
    response = await api_client.get("/entitlements/")

    assert response.status_code == 200
    data = response.json()

    assert data["total"] == 2
    assert len(data["items"]) == data["total"]

    assert_json_contains_model(data, entitlement_aws)
    assert_json_contains_model(data, entitlement_gcp)
