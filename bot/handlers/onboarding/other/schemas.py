from pydantic import BaseModel
from typing import Literal


class OtherQuestionInfo(BaseModel):
    type: Literal["write_to_chat", "call"]
