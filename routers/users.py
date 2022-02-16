from uuid import UUID
from pydantic import BaseModel
from fastapi import APIRouter, Depends, Request, UploadFile, File
from sqlalchemy.orm import Session
from services.database import get_db
from services.auth import get_current_user, check_duplicate, get_current_admin_user
from services.exceptions import duplicate_exception, invalid_exception
from services.minio import upload_image_file
from schemas.users import UserProfile, UserList
from models import User

user_router = APIRouter(prefix="/user")

class CheckDuplicate(BaseModel):
    email: str = None
    phone: str = None
    username: str = None


@user_router.get("/me", response_model=UserProfile)
async def get_my_profile(
    user: User = Depends(get_current_user)
):
    return user


@user_router.post("/me", response_model=UserProfile)
async def update_my_profile(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """
        {
            "name": str,
            "username": str,
            "email": str,
            "phone": str,
            "dob": datetime,
        }
    """
    data = await request.json() or {}

    if data is {}:
        return user
  
    user_data = UserProfile(**data)
    
    user.name = user_data.name
    user.username = user_data.username
    user.email = user_data.email
    user.phone = user_data.phone
    user.dob = user_data.dob
    
    try:
        db.commit()
    except:
        raise duplicate_exception
    return user


@user_router.get("/id/{user_id}", response_model=UserProfile)
async def user_profile(
    user_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    user = db.query(User).filter_by(id=user_id).first()
    return user


@user_router.post("/check_duplicate")
async def check_credential(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """
        "username": Optional[str],
        "email": Optional[str],
        "phone": Optional[str]
    """

    data = await request.json() or {}

    if data is {}:
        raise invalid_exception
    
    check_data = CheckDuplicate(**data)

    is_duplicate = check_duplicate(
        db,
        id = user.id,
        email = check_data.email,
        username = check_data.username,
        phone = check_data.phone 
    )

    if is_duplicate:
        raise duplicate_exception
    return {
        "message": "Username, phone or email is available"
    }


@user_router.post("/profile_picture")
async def update_profile_picture(
    user: User = Depends(get_current_user),
    file: UploadFile = File(...)
):
    bucket_name = "profile-picture"
    image_name = f"{user.id}"
    return await upload_image_file(bucket_name, file, image_name)


# Admin Module for Users
@user_router.get("/all", response_model=UserList)
def get_all_users(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_admin_user)
):
    user_list = db.query(User).all()

    return UserList(data=user_list)
