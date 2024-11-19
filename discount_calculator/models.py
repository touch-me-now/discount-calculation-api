from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from discount_calculator.contexts import DiscountBaseContext
from discount_calculator.enums import DiscountType
from discount_calculator.strategies.base import BaseDiscountStrategy


class DiscountCalculator(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    strategy: BaseDiscountStrategy
    context: DiscountBaseContext

    def calculate(self, amount: Decimal):
        return self.strategy.execute(amount, self.context)

    @property
    def discount_type(self) -> DiscountType:
        return self.strategy.discount_type


class DiscountItem(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    original_amount: Decimal
    quantity_discount: Decimal = Decimal("0.00")
    loyalty_discount: Decimal = Decimal("0.00")
    final_amount: Decimal = None
    applied_discounts: list[DiscountType] = []

    def model_post_init(self, __context):
        if self.final_amount is None:
            self.final_amount = self.original_amount
