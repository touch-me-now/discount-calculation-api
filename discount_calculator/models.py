from decimal import Decimal

from pydantic import BaseModel

from discount_calculator.contexts import DiscountBaseContext
from discount_calculator.enums import DiscountType
from discount_calculator.strategies.base import BaseDiscountStrategy


class DiscountCalculator(BaseModel):
    name: str
    strategy: BaseDiscountStrategy
    context: DiscountBaseContext

    class Config:
        arbitrary_types_allowed = True

    def calculate(self, amount: Decimal):
        return self.strategy.execute(amount, self.context)

    @property
    def discount_type(self) -> DiscountType:
        return self.strategy.discount_type


class DiscountItem(BaseModel):
    original_amount: Decimal
    quantity_discount: Decimal
    loyalty_discount: Decimal
    final_amount: Decimal
    applied_discounts: list[DiscountType]

    class Config:
        use_enum_values = True
