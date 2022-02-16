from lib2to3.pytree import Base
from fastapi import APIRouter, Depends, Request, File, UploadFile, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID

from services.database import get_db
from services.auth import get_current_user
from services.exceptions import invalid_exception
from services.minio import upload_image_file
from schemas.users import UserProfile, TeamMembersProfile
from schemas.teams import TeamProfile, TeamList

from models import User, Team, TeamMember
team_router = APIRouter(prefix="/teams")


class CreateTeamRequest(BaseModel):
    name: str
    logo_url: Optional[str]

class CreateTeamMembers(BaseModel):
    user_id: UUID
    team_id: UUID
    
class TeamMembers(BaseModel):
    user: UserProfile
    team: TeamProfile

    class Config:
        orm_mode = True

class TeamMemberRequest(BaseModel):
    data: List[UserProfile]

def create_team_member(name: str, email: str, db: Session):
    new_member = User(name=name, email=email)

    try:
        db.add(new_member)
        db.commit()
        db.refresh(new_member)
        return new_member
    except:
        raise invalid_exception

def add_member_to_team(user_id: UUID, team_id: UUID, db: Session):
    team_member = TeamMember(user_id=user_id, team_id=team_id)

    try:
        db.add(team_member)
        db.commit()
        db.refresh(team_member)
        return team_member
    except:
        print("Failed adding team members")
        raise invalid_exception


@team_router.post("/team_logo")
async def upload_team_logo(
    user: User = Depends(get_current_user),
    file: UploadFile = File(...),
    team_name: str = Form(...)
):
    bucket_name = "team-logo"
    return await upload_image_file(bucket_name, file, team_name)


@team_router.post("/", response_model=TeamProfile)
async def create_new_team(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """
        {
            "name": str,
            "logo_url": Optional[str]
        }
    """
    data = await request.json() or {}

    if data is {}:
        raise invalid_exception

    team_req = CreateTeamRequest(**data)
    new_team = Team(**team_req.dict())
    user.teams.append(new_team)
    try:
        db.add_all([new_team, user])
        db.commit()
        db.refresh(new_team)
        return new_team
    except:
        raise invalid_exception


@team_router.get("/my_team", response_model=TeamList)
async def get_all_team(
    user: User = Depends(get_current_user)
):
    return TeamList(data=user.teams)


@team_router.get("/id/{team_id}", response_model=TeamMembersProfile)
async def get_team_by_id(
    team_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    team_detail = db.query(Team).filter_by(id=team_id).first()

    return team_detail


@team_router.post("/add_members/{team_id}", response_model=TeamMembersProfile)
async def add_team_members(
    team_id: UUID,
    request: Request,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
        {
            data: [User]
        }
    """

    data = await request.json() or {}

    if data is {}:
        raise invalid_exception
    
    new_team_request = TeamMemberRequest(**data)

    for member in new_team_request.data:
        # TODO: Check if its not new member
        new_member = create_team_member(name=member.name, email=member.email, db=db)
        add_member_to_team(new_member.id, team_id, db)


    team_detail = db.query(Team).filter_by(id=team_id).first()

    return team_detail

