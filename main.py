from decimal import Decimal

from fastapi import FastAPI
from pydantic import BaseModel, Field
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


@app.post("/api/calculate-discount/", status_code=status.HTTP_200_OK)
def calculate_discount(
    form_data: CalculationInput,
) -> DiscountItem:
    """
    calculates discounts in the cart based on the order amount and customer loyalty status.
    """
    return calculate_discounts(
        amount=form_data.amount,
        is_loyal=form_data.is_loyal,
        min_amount=settings.min_quantity_amount
    )
