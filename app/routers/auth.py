from fastapi import APIRouter
from app.db.schemas.user import UserCreate, UserLogin

router = APIRouter()


@router.post("/login")
def login(loginDetails: UserLogin):
    return {"data": "login"}


@router.post("/signup")
def signup(signupDetails: UserCreate):
    return {"data": "signup"}
