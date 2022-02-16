from pydantic import BaseModel, UUID4
from typing import List

class CountryItem(BaseModel):
    id: UUID4
    code: str
    name: str
    phone_code: str

    class Config:
        orm_mode = True


class CountryItemsList(BaseModel):
    data: List[CountryItem]

    class Config:
        orm_mode = True