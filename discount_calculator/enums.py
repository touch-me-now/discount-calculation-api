from enum import Enum


class DiscountType(str, Enum):
    QUANTITY = 'quantity'
    LOYALTY = 'loyalty'
