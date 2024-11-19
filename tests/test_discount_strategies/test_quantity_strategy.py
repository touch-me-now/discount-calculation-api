from decimal import Decimal

from discount_calculator import QuantityDiscountStrategy, QuantityContext


def test_quantity_discount_applied():
    strategy = QuantityDiscountStrategy(discount_percent=Decimal("10.00"))
    context = QuantityContext(min_amount=Decimal("100.00"))
    amount = Decimal("150.00")

    discount = strategy.execute(amount, context)

    assert discount == Decimal("15.00")  # 10% from 150


def test_quantity_discount_not_applied():
    strategy = QuantityDiscountStrategy(discount_percent=Decimal("10.00"))
    context = QuantityContext(min_amount=Decimal("200.00"))  # The minimum amount is higher than the current one
    amount = Decimal("150.00")

    discount = strategy.execute(amount, context)

    assert discount == Decimal("0.00")
