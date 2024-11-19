from decimal import Decimal

from discount_calculator import calculate_discounts
from discount_calculator.models import DiscountItem


def test_success_calculate_discounts():
    item = calculate_discounts(
        amount=Decimal("150.00"),
        is_loyal=True,
        min_amount=Decimal("100.00")
    )

    assert isinstance(item, DiscountItem)
    assert item.original_amount == Decimal("150.00")
    assert item.quantity_discount == Decimal("15.00")
    assert item.loyalty_discount == Decimal("7.50")
    assert item.final_amount == Decimal("127.50")
    assert item.applied_discounts == ['quantity', 'loyalty']


def test_empty_params_calculation():
    item = calculate_discounts(
        amount=Decimal("150.00"),
        is_loyal=None,   # must be None or False to disable loyalty
        min_amount=None  # must be None to disable quantity
    )

    expected = DiscountItem(
        original_amount=Decimal('150.00'),
        quantity_discount=Decimal('0.00'),
        loyalty_discount=Decimal('0.00'),
        final_amount=Decimal('150.00'),
        applied_discounts=[]
    )

    assert expected == item


def test_only_loyalty():
    item = calculate_discounts(
        amount=Decimal("150.00"),
        is_loyal=True,
        min_amount=None  # must be None to disable quantity
    )

    assert ['loyalty'] == item.applied_discounts

    expected = DiscountItem(
        original_amount=Decimal('150.00'),
        quantity_discount=Decimal('0.00'),
        loyalty_discount=Decimal('7.50'),
        final_amount=Decimal('142.50'),
        applied_discounts=[
            'loyalty'
        ]
    )
    assert expected == item


def test_only_quantity():
    item = calculate_discounts(
        amount=Decimal("150.00"),
        is_loyal=None,
        min_amount=Decimal("100.00")  # must be None to disable quantity
    )

    assert ['quantity'] == item.applied_discounts

    expected = DiscountItem(
        original_amount=Decimal('150.00'),
        quantity_discount=Decimal('15.00'),
        loyalty_discount=Decimal('0.00'),
        final_amount=Decimal('135.00'),
        applied_discounts=[
            'quantity'
        ]
    )
    assert expected == item


def test_quantity_dont_execute_on_less():
    item = calculate_discounts(
        amount=Decimal("99.99"),
        is_loyal=None,
        min_amount=Decimal("100.00")  # must be None to disable quantity
    )

    assert 'quantity' not in item.applied_discounts

    expected = DiscountItem(
        original_amount=Decimal('99.99'),
        quantity_discount=Decimal('0.00'),
        loyalty_discount=Decimal('0.00'),
        final_amount=Decimal('99.99'),
        applied_discounts=[]
    )
    assert expected == item

    equal_amount_item = calculate_discounts(
        amount=Decimal("100.00"),
        is_loyal=None,
        min_amount=Decimal("100.00")  # must be None to disable quantity
    )

    assert equal_amount_item.original_amount == Decimal("100.00")
