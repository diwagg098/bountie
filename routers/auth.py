from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime

from services.database import get_db
from services.auth import (
    create_access_token,
    get_user,
    get_password_hash,
    verify_password,
    get_current_user
)
from services.exceptions import (
    invalid_exception,
    credential_exception,
    verified_exception,
    user_registered_exception
)

from models import User


auth_router = APIRouter(prefix="/auth")

class UserLoginRequest(BaseModel):
    email: str = None
    phone: str = None
    username: str = None
    password: str

class UserRegisterRequest(BaseModel):
    name: str
    username: str
    email: str
    phone: str
    password: str

class ResetPassword(BaseModel):
    old_password: str
    new_password: str


@auth_router.post("/login")
async def login_user(
    request: Request,
    db: Session = Depends(get_db)
):
    """
        {
            "email": str,
            "phone": str,
            "username": str,
            "password": str
        }
    """

    data = await request.json() or {}
    
    if data is {}:
        raise invalid_exception

    login_request = UserLoginRequest(**data)

    if login_request.email is None and login_request.phone is None:
        raise invalid_exception
    
    user: User = get_user(
        db, 
        email = login_request.email,
        phone = login_request.phone)
    if not user:
        raise credential_exception

    if verify_password(login_request.password, user.password):
        access_token = create_access_token(data = {"sub": str(user.id)})
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    raise credential_exception

@auth_router.post("/register")
async def register_user(
    request: Request,
    db: Session = Depends(get_db)
):
    """
        {
            "name": str,
            "email": str,
            "phone": str,
            "password": str,
            "username": str
        }
    """
    data = await request.json() or {}

    if data is {}:
        raise invalid_exception
    
    register_request = UserRegisterRequest(**data)

    user: User = get_user(
        db,
        email = register_request.email,
        username = register_request.username,
        phone = register_request.phone)
    if not user:
        new_user = User(**register_request.dict())
        new_user.password = get_password_hash(new_user.password)
        db.add(new_user)
        db.commit()
        return {"id": new_user.id}
    raise user_registered_exception


@auth_router.post("/reset-password")
async def reset_password(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """
        "old_password": str,
        "new_password": str
    """

    data = await request.json() or {}

    if data is {}:
        raise invalid_exception
    
    password_req = ResetPassword(**data)

    if verify_password(password_req.old_password, user.password):
        user.password = get_password_hash(password_req.new_password)
        try:
            db.commit()
            return {
                "message": "Password sucessfully updated"
            }
        except:
            raise invalid_exception
    
    raise credential_exception



@auth_router.get("/verify/{verify_token}")
async def verify_email(
    verify_token: str,
    db: Session = Depends(get_db)
):
    # TODO: verify token string on redis
    # TODO: if verified, update the database status based on user id
    # TODO: remove the token from redis
    # TODO: return the status as success, else invalid token
    pass
