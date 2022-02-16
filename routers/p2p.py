from typing import Optional, List
from pydantic import BaseModel, UUID4
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from services.database import get_db
from services.exceptions import invalid_exception
from services.auth import get_current_admin_user
from models import P2PCust, P2PAgent, User, P2PListing, Token
p2p_router = APIRouter(prefix="/p2p")


class ContactRequest(BaseModel):
    name: str
    phone: str
    email: Optional[str]


class AgentRequest(BaseModel):
    name: str
    phone: str
    telegram: str
    country_code: str


class AgentResponse(AgentRequest):
    id: UUID4
    active: bool

    class Config:
        orm_mode = True


class ListingRequest(BaseModel):
    price: int
    max_amount: int
    payment_method: str
    agent_id: UUID4
    token_symbol: str


class ListingResponse(ListingRequest):
    id: UUID4

    class Config:
        orm_mode = True


class AllListings(BaseModel):
    data: List[ListingResponse]


class AgentListResponse(BaseModel):
    data: List[AgentResponse]


class ContactResponse(ContactRequest):
    id: UUID4


@p2p_router.get("/agents", response_model=AgentListResponse)
async def get_agents(
    db: Session = Depends(get_db)
):
    agent_list = db.query(P2PAgent).filter_by(active=True).all()

    return AgentListResponse(data=agent_list)


@p2p_router.post("/agents", response_model=AgentResponse)
async def create_agent(
    request: Request,
    user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
        {
            "name": str,
            "phone": str,
            "telegram": str,
            "country_code": str
        }
    """
    data = await request.json() or {}

    if data is {}:
        raise invalid_exception

    agent_data = AgentRequest(**data)
    new_agent = P2PAgent(**agent_data.dict())

    try:
        db.add(new_agent)
        db.commit()
        db.refresh(new_agent)
        return new_agent
    except:
        raise invalid_exception


@p2p_router.get("/listings", response_model=AllListings)
async def get_listings(
    db: Session = Depends(get_db)
):

    listing_data = db.query(P2PListing).filter(P2PListing.max_amount > 0).all()

    return AllListings(data=listing_data)


@p2p_router.post("/listings", response_model=AllListings)
async def get_listings(
    db: Session = Depends(get_db)
):

    listing_data = db.query(P2PListing).filter(P2PListing.max_amount > 0).all()

    return AllListings(data=listing_data)


@p2p_router.post("/contact", response_model=ContactResponse)
async def create_contact(
    request: Request,
    db: Session = Depends(get_db)
):
    """
        "name": str,
        "phone: str,
        "email: str
    """

    data = await request.json() or {}

    if data is {}:
        raise invalid_exception

    p2p_req = ContactRequest(**data)

    new_contact = P2PCust(**p2p_req.dict())

    try:
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)
        return new_contact
    except:
        raise invalid_exception
