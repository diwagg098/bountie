from typing import List
from datetime import datetime
from pydantic import BaseModel, UUID4
from fastapi import APIRouter, Depends, Request, File, Form, UploadFile
from sqlalchemy.orm import Session
from services.auth import get_current_admin_user, get_current_active_user
from services.database import get_db
from services.minio import upload_image_file
from services.exceptions import invalid_exception
from models import User, Promotion

promotion_router = APIRouter(prefix="/promotions")


class PromotionItemRequest(BaseModel):
    name: str
    banner_url: str
    tnc: str
    start_date: datetime
    end_date: datetime
    amount: int

    class Config:
        orm_mode = True

class PromotionItem(PromotionItemRequest):
    id: UUID4

class PromotionList(BaseModel):
    data: List[PromotionItem]


@promotion_router.post("/banner")
async def upload_banner(
    user: User = Depends(get_current_admin_user),
    file: UploadFile = File(...),
    image_name: str = Form(...)
):
    return await upload_image_file("promotion-banner", file, image_name)


@promotion_router.get("/active", response_model=PromotionList)
async def active_promotion(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user)
):
    promotion_list = db.query(Promotion).filter(Promotion.end_date>= datetime.now()).all()
    
    return PromotionList(data=promotion_list)

