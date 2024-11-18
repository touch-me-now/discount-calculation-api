from decimal import Decimal
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent


class Settings(BaseSettings, frozen=True):
    quantity_discount_name: str = "quantity_discount"
    loyalty_discount_name: str = "loyalty_discount"
    quantity_discount_percent: Decimal = Decimal("10.00")
    loyalty_discount_percent: Decimal = Decimal("5.00")

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env")


settings = Settings()
