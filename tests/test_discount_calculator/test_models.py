from decimal import Decimal

from discount_calculator.models import DiscountItem


def test_final_amount_is_not_none():
    # final_amount can be set like None
    item = DiscountItem(original_amount=Decimal("100.00"), final_amount=None)

    # after initialize must be equal to original_amount
    assert item.final_amount is not None
    assert item.final_amount == item.original_amount
