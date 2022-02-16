from pydantic import BaseModel, UUID4
from typing import List

class GameRequest(BaseModel):
    image_url: str
    name: str
    description: str
    featured: bool

class GameItem(GameRequest):
    id: UUID4

    class Config:
        orm_mode = True


class GamesList(BaseModel):
    data: List[GameItem]

    class Config:
        orm_mode = True