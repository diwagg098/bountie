from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel

from services.database import get_db
from services.auth import get_current_admin_user
from services.exceptions import invalid_exception
from models import Country, User
from schemas.countries import CountryItemsList, CountryItem

countries_router = APIRouter(prefix="/countries")


class CountryRequest(BaseModel):
    code: str
    name: str
    phone_code: str


@countries_router.get("/", response_model=CountryItemsList)
def get_countries_list(
    db: Session = Depends(get_db)
):

    countries_list = db.query(Country).all()

    return CountryItemsList(data=countries_list)


@countries_router.post("/", response_model=CountryItem)
async def add_country(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_admin_user)
):
    """
        "code": str,
        "name: str,
        "phone_code": str
    """

    data = await request.json() or {}

    if data is {}:
        raise invalid_exception

    country_req = CountryRequest(**data)
    new_country = Country(**country_req.dict())
    try:
        db.add(new_country)
        db.commit()
        db.refresh(new_country)
        return new_country
    except:
        raise invalid_exception
