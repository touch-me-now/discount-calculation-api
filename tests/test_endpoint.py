import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@pytest.mark.parametrize(
    "payload, expected_response",
    [
        # No quantity discount
        (
            # input
            {
                "amount": "50.00",
                "is_loyal": False,
                "cart_items": [
                    {"id": 1, "quantity": 1, "price": "50.00"}
                ],
            },
            # expected output
            {
                "original_amount": "50.00",
                "quantity_discount": "0.00",
                "loyalty_discount": "0.00",
                "final_amount": "50.00",
                "applied_discounts": [],
            },
        ),
        # With quantity discount
        (
            # input
            {
                "amount": "150.00",
                "is_loyal": False,
                "cart_items": [
                    {"id": 1, "quantity": 2, "price": "50.00"},
                    {"id": 2, "quantity": 1, "price": "50.00"}
                ],
            },
            # expected output
            {
                "original_amount": "150.00",
                "quantity_discount": "15.00",
                "loyalty_discount": "0.00",
                "final_amount": "135.00",
                "applied_discounts": ["quantity"],
            },
        ),
        # With quantity and loyalty discounts
        (
            # input
            {
                "amount": "150.00",
                "is_loyal": True,
                "cart_items": [
                    {"id": 1, "quantity": 2, "price": "50.00"},
                    {"id": 2, "quantity": 1, "price": "50.00"}
                ],
            },
            # expected output
            {
                "original_amount": "150.00",
                "quantity_discount": "15.00",
                "loyalty_discount": "6.75",
                "final_amount": "128.25",
                "applied_discounts": ["quantity", "loyalty"],
            },
        ),
    ],
)
def test_calculate_discount(payload, expected_response):
    response = client.post("/api/calculate-discount/", json=payload)
    assert response.status_code == 200, response.json()

    print(response.json())
    print(expected_response)

    assert response.json() == expected_response, response.json()
