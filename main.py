from routers.p2p import p2p_router
from routers.promotions import promotion_router
from routers.vouchers import voucher_router
from routers.teams import team_router
from routers.games import games_router
from routers.users import user_router
from routers.auth import auth_router
from routers.countries import countries_router
from services.database import get_db
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(countries_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(games_router)
app.include_router(team_router)
app.include_router(voucher_router)
app.include_router(promotion_router)
app.include_router(p2p_router)


@app.get("/")
def main(db=Depends(get_db)):
    return {"message": "Hello world"}
