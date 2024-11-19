from copy import copy
from decimal import Decimal

from config import settings
from discount_calculator.contexts import QuantityContext, LoyaltyContext
from discount_calculator.models import DiscountCalculator, DiscountItem
from discount_calculator.strategies import QuantityDiscountStrategy, LoyaltyDiscountStrategy


def calculate_discounts(amount: Decimal, is_loyal: bool | None = None, min_amount: Decimal | None = None):
    """
    Calculates discounts based on the passed parameters.
    This is the main function with list as calculation queue.
    With the proper parameters, strategy will be added to the list and executed one by one.

    :param amount: Decimal
        Total order amount before discounts are applied.
        Example: Decimal("150.00")

    :param is_loyal: bool
        Indicates whether the customer is loyal.
        - True: loyal customer (may receive a discount for loyalty).
        - False: customer is not loyal.
        Example: True

    :param min_amount:
        Minimum order amount required for quantity discount to apply.
        Example: Decimal("100.00")

    :return: DiscountItem
        An object containing detailed information about applied discounts:
        - `original_amount`: original order amount before discounts.
        - `quantity_discount`: quantity discount amount (if applicable).
        - `loyalty_discount`: loyalty discount amount (if applicable).
        - `final_amount`: final order amount after all discounts.
        - `applied_discounts`: list of discount types applied (e.g. ["quantity", "loyalty"]).
    """
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
