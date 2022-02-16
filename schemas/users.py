from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, validator
from typing import List
from schemas.teams import TeamProfile

class TokenData(BaseModel):
    user_id: UUID


class UserProfile(BaseModel):
    name: str = None
    username: str = None
    email: str = None
    phone: str = None
    dob: datetime = None

    class Config:
        orm_mode = True
    
    @validator('dob', pre=True)
    def validate_time(cls, v):
        if type(v) == datetime or v is None:
            return v
        return datetime.strptime(v, "%Y-%M-%d")

class UserList(BaseModel):
    data: List[UserProfile]

class UserProfileTeams(UserProfile):
     teams: List[TeamProfile] = []

class TeamMembersProfile(TeamProfile):
    members: List[UserProfile]