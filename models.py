from pydantic import BaseModel
from typing import List

class WaitlistEntry(BaseModel):
    name: str = ""
    email: str = ""
    profession: str = ""
    meetupPlaces: List[str] = []
    frequency: str = ""
    interests: str = ""
    reason: str = ""