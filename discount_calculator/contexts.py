from decimal import Decimal

from pydantic import BaseModel


class DiscountBaseContext(BaseModel):
    pass


class QuantityContext(DiscountBaseContext):
    min_amount: Decimal


class LoyaltyContext(DiscountBaseContext):
    is_loyal: bool = False
