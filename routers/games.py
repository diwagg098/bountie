from typing import Optional
from fastapi import APIRouter, Depends, Request, File, UploadFile, Form
from sqlalchemy.orm import Session
from services.database import get_db
from services.auth import get_current_admin_user
from services.exceptions import invalid_exception
from services.minio import upload_image_file
from models import Game, User
from schemas.games import GamesList, GameItem, GameRequest

games_router = APIRouter(prefix="/games")


@games_router.get("/")
def get_all_games(
    featured: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    if featured is None:
        games_list = db.query(Game).all()
    else:
        print("Filtering")
        games_list = db.query(Game).filter_by(featured=featured).all()
    return GamesList(data=games_list)


@games_router.post("/upload_logo")
async def upload_logo(
    user: User = Depends(get_current_admin_user),
    file: UploadFile = File(...),
    image_name: str = Form(...)
):
    bucket_name = "games-logo"
    return await upload_image_file(bucket_name, file, image_name)


@games_router.post("/", response_model=GameItem)
async def create_new_game(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_admin_user)
):
    """
        {
            "name": str,
            "image_url": str,
            "description": str, 
            "featured": bool
        }
    """

    data = await request.json() or {}

    if data is {}:
        raise invalid_exception

    game_req = GameRequest(**data)
    new_game = Game(**game_req.dict())

    try:
        db.add(new_game)
        db.commit()
        db.refresh(new_game)
        return new_game
    except:
        raise invalid_exception
