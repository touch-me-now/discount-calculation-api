from abc import abstractmethod
from decimal import Decimal

from discount_calculator.contexts import DiscountBaseContext
from discount_calculator.enums import DiscountType


class BaseDiscountStrategy:
    discount_type: DiscountType = None

    def __init__(self, discount_percent: Decimal):
        if not isinstance(self.discount_type, DiscountType):
            raise TypeError(f"Expected `discount_type` to be an instance of `{DiscountType.__name__}`")

        self.discount_percent = discount_percent

    @abstractmethod
    def execute(self, amount: Decimal, context: DiscountBaseContext) -> Decimal:
        raise NotImplemented(f'`calculate` must be implemented for {self.__class__.__name__}!')
