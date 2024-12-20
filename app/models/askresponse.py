from pydantic import BaseModel
from typing import Optional


class AskResponse(BaseModel):
    query: str
    response: str
    groundedness: Optional[float]
    