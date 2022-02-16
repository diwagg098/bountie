from pydantic import BaseModel
from uuid import UUID
from typing import List

class TeamProfile(BaseModel):
    id: UUID
    name: str
    logo_url: str = None
    
    class Config:
        orm_mode = True

class TeamList(BaseModel):
    data: List[TeamProfile]