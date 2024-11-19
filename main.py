from decimal import Decimal
from typing import Self

from fastapi import FastAPI
from pydantic import BaseModel, Field, model_validator
from starlette import status

from config import settings
from discount_calculator import calculate_discounts
from discount_calculator.models import DiscountItem


app = FastAPI(
    debug=settings.debug,
    title="Discount calculation API",
    version="0.1.0"
)


class CartItem(BaseModel):
    id: int
    quantity: int = Field(ge=1)
    price: Decimal = Field(ge=0.01, decimal_places=2)


class CalculationInput(BaseModel):
    amount: Decimal = Field(ge=0.01, decimal_places=2)
    is_loyal: bool = False
    cart_items: list[CartItem] = None

    @property
    def cart_amount(self) -> Decimal:
        return sum([item.price * item.quantity for item in self.cart_items or []])

    @model_validator(mode='after')
    def check_amount(self) -> Self:
        if self.amount != self.cart_amount:
            raise ValueError('amount do not match with cart items amount')
        return self


@app.post(
    "/api/calculate-discount/",
    response_model=DiscountItem,
    status_code=status.HTTP_200_OK,
    summary="Calculate discounts based on order total and loyalty status",
    response_description="Returns the final amount with applicable discounts",
)
def calculate_discount(
    form_data: CalculationInput,
) -> DiscountItem:
    """
    Calculates discounts in the cart based on the order amount and customer loyalty.

    **Request Example:**
    ```json
    {
        "amount": "150.00",
        "is_loyal": true,
        "cart_items": [
            {"id": 1, "quantity": 2, "price": "50.00"},
            {"id": 2, "quantity": 1, "price": "50.00"}
        ]
    }
    ```

    **Response Example:**
    ```json
    {
        "original_amount": "150.00",
        "quantity_discount": "15.00",
        "loyalty_discount": "6.75",
        "final_amount": "128.25",
        "applied_discounts": ["quantity", "loyalty"]
    }
    ```
    """
    return calculate_discounts(
        amount=form_data.amount,
        is_loyal=form_data.is_loyal,
        min_amount=settings.min_quantity_amount
    )
