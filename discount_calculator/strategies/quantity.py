from decimal import Decimal

from discount_calculator.contexts import QuantityContext
from discount_calculator.enums import DiscountType
from discount_calculator.strategies.base import BaseDiscountStrategy
from discount_calculator.utils import percent_part_amount, into_monetary_format


class QuantityDiscountStrategy(BaseDiscountStrategy):
    """
    If total amount > minimum amount then the percentage of total amount is calculated
    """
    discount_type = DiscountType.QUANTITY

    def execute(self, amount: Decimal, context: QuantityContext) -> Decimal:
        if amount > context.min_amount:
            discount_amount = percent_part_amount(amount, percent=self.discount_percent)
        else:
            discount_amount = Decimal(0)
        return into_monetary_format(discount_amount)
