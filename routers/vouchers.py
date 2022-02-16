from typing import List
from datetime import datetime
from pydantic import BaseModel, UUID4
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from services.auth import get_current_admin_user, get_current_active_user
from services.database import get_db
from services.exceptions import invalid_exception
from models import User, Voucher

voucher_router = APIRouter(prefix="/vouchers")


class VoucherItemRequest(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime
    amount: int

    class Config:
        orm_mode = True

class VoucherItem(VoucherItemRequest):
    id: UUID4

class VoucherList(BaseModel):
    data: List[VoucherItem]


@voucher_router.get("/active", response_model=VoucherList)
async def all_vouchers(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user)
):
    voucher_list = db.query(Voucher).filter(Voucher.end_date>= datetime.now()).all()
    
    return VoucherList(data=voucher_list)


@voucher_router.post("/", response_model=VoucherItem)
async def create_voucher(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_admin_user)
):
    """
        {
            "name": str, 
            "amount": int,
            "start_date": datetime,
            "end_date": datetime
        }
    """
    data = await request.json() or {}

    if data is {}:
        raise invalid_exception
    
    voucher_item = VoucherItemRequest(**data)
    new_voucher = Voucher(**voucher_item.dict())

    try:
        db.add(new_voucher)
        db.commit()
        db.refresh(new_voucher)
        return new_voucher
    except:
        raise invalid_exception

