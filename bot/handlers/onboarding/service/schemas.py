from pydantic import BaseModel
from typing import Optional, Literal


class ServiceRepairInfo(BaseModel):
    type: Literal["boost", "best"]
    registration_number: Optional[str] = None
    vin: Optional[str] = None
    mileage: Optional[int] = None
    problem_description: Optional[str] = None
