from pydantic import BaseModel
from typing import Optional


class InsuranceInfo(BaseModel):
    registration_number: Optional[str] = None
    vin: Optional[str] = None
