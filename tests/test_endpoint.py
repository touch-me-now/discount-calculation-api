import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from main import app


@pytest_asyncio.fixture(scope="function")
async def api_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_cli:
        yield async_cli


@pytest.mark.asyncio
async def test_success_calculation_request(api_client: AsyncClient):
    response = await api_client.post(
        "/api/calculate-discount/",
        json={
            "amount": "150.00",
            "is_loyal": True
        }
    )
    assert response.status_code == 200, response.json()


