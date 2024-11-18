from decimal import Decimal

from discount_calculator.contexts import LoyaltyContext
from discount_calculator.enums import DiscountType
from discount_calculator.strategies.base import BaseDiscountStrategy
from discount_calculator.utils import percent_part_amount, into_monetary_format


class LoyaltyDiscountStrategy(BaseDiscountStrategy):
    discount_type = DiscountType.LOYALTY

    def execute(self, amount: Decimal, context: LoyaltyContext) -> Decimal:
        if context.is_loyal is True:
            discount_amount = percent_part_amount(amount, percent=self.discount_percent)
        else:
            discount_amount = Decimal(0)
        return into_monetary_format(discount_amount)
