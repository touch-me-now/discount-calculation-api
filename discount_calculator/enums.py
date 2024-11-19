from enum import Enum


class DiscountType(str, Enum):
    """Types of discounts"""
    QUANTITY = 'quantity'
    LOYALTY = 'loyalty'
