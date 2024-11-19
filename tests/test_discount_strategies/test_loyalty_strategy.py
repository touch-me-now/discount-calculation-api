from decimal import Decimal

from discount_calculator import LoyaltyDiscountStrategy, LoyaltyContext


def test_loyalty_discount_applied():
    strategy = LoyaltyDiscountStrategy(discount_percent=Decimal("5.00"))
    context = LoyaltyContext(is_loyal=True)
    amount = Decimal("150.00")

    discount = strategy.execute(amount, context)

    assert discount == Decimal("7.50")  # 5% from 150


def test_loyalty_discount_not_applied():
    strategy = LoyaltyDiscountStrategy(discount_percent=Decimal("5.00"))
    context = LoyaltyContext(is_loyal=False)
    amount = Decimal("150.00")

    discount = strategy.execute(amount, context)

    assert discount == Decimal("0.00")
