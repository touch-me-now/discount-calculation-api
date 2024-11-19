from decimal import Decimal

from discount_calculator.models import DiscountItem


def test_final_amount_none():
    item = DiscountItem(original_amount=Decimal("100.00"), final_amount=None)

    assert item.final_amount == item.original_amount
