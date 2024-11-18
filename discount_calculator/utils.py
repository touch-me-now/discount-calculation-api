from decimal import Decimal, ROUND_HALF_UP


def into_monetary_format(decimal: Decimal) -> Decimal:
    return decimal.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def percent_part_amount(amount: Decimal, percent: Decimal):
    return amount * (percent / Decimal(100))
