from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

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
    """output model after calculating discounts """
    model_config = ConfigDict(use_enum_values=True)

    original_amount: Decimal = Field(description="Initial order amount")
    quantity_discount: Decimal = Field(Decimal("0.00"), description="Calculated quantity discount amount")
    loyalty_discount: Decimal = Field(Decimal("0.00"), description="Calculated loyalty discount amount")
    final_amount: Decimal | None = Field(None, description="Order amount after deducting all discounts")
    applied_discounts: list[DiscountType] = Field([], description="types of discounts that have been applied")

    def model_post_init(self, __context):
        if self.final_amount is None:
            self.final_amount = self.original_amount
