from copy import copy
from decimal import Decimal

from config import settings
from discount_calculator.contexts import QuantityContext, LoyaltyContext
from discount_calculator.models import DiscountCalculator, DiscountItem
from discount_calculator.strategies import QuantityDiscountStrategy, LoyaltyDiscountStrategy


def calculate_discounts(amount: Decimal, is_loyal: bool = None, min_amount: Decimal = None):
    discount_calculators = []

    if min_amount:
        discount_calculators.append(
            DiscountCalculator(
                name=settings.quantity_discount_name,
                strategy=QuantityDiscountStrategy(discount_percent=settings.quantity_discount_percent),
                context=QuantityContext(min_amount=min_amount)
            )
        )

    if is_loyal:
        discount_calculators.append(
            DiscountCalculator(
                name=settings.loyalty_discount_name,
                strategy=LoyaltyDiscountStrategy(discount_percent=settings.loyalty_discount_percent),
                context=LoyaltyContext(is_loyal=is_loyal)
            )
        )

    copied_amount = copy(amount)
    applied, collected_amounts = [], {}

    for calculator in discount_calculators:
        discount_amount = calculator.calculate(copied_amount)
        collected_amounts[calculator.name] = discount_amount

        if discount_amount > 0:
            copied_amount -= discount_amount
            applied.append(calculator.discount_type)

    return DiscountItem(
        original_amount=amount,
        final_amount=copied_amount,
        applied_discounts=applied,
        **collected_amounts
    )
