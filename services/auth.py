import random
from os import getenv
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql.base import UUID
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.sql.expression import false

from services.database import get_db
from models import User
from schemas.users import TokenData

from .exceptions import (
    credential_exception,
    inactive_exception,
    admin_exception
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = getenv("ALGORITHM")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def generate_otp():
    return random.randint(1000,9999)


def verify_otp(input_otp, saved_otp):
    return input_otp == saved_otp


async def send_phone_otp(db: Session, phone: str, otp: int):
    print(f'Sending email to {phone} with OTP number {otp}')
    # TODO: send OTP Here using email


def get_user(db: Session, id: UUID = None, email: str = None, username: str = None, phone: str = None):
    user = db.query(User).filter(
        (User.id == id) |
        (User.email == email) | 
        (User.username == username) | 
        (User.phone == phone)).first()
    return user

def check_duplicate(db: Session, id: UUID = None, email: str = None, username: str = None, phone: str = None):
    user = db.query(User).filter(
        (User.id != id) &
        (User.email == email) | 
        (User.username == username) | 
        (User.phone == phone)).first()
    
    print(user)
    if user:
        return True
    return False

async def authenticate_user(db: Session, otp: int, user_id: UUID):
    user = get_user(db=db, user_id=user_id)
    if not user:
        return False
    
    return True


def create_access_token(data: dict):
    to_encode = data.copy()
    expiry = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expiry})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credential_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credential_exception
    
    user = get_user(db=db, id=token_data.user_id)
    if user is None:
        raise credential_exception
    return user


async def get_current_active_user(current_user=Depends(get_current_user)):
    # if not current_user.status == UserStatusEnum.ACTIVE:
    #     raise inactive_exception
    return current_user


async def get_current_admin_user(current_user=Depends(get_current_user)):
    if current_user.is_admin:
        return current_user
    raise admin_exception