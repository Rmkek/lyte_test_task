from decimal import Decimal

from sqlmodel import Field, SQLModel


class Tier(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    price: Decimal
    transfer_fee_percent: Decimal
