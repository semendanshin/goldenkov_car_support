from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, NamedTuple, Literal


class BuyOrSellCarInfo(BaseModel):
    option: Literal['buy', 'sell']
    vin: Optional[str] = None
    registration_number: Optional[str] = None
    mileage: Optional[int] = None
    brand_and_model: Optional[str] = None
