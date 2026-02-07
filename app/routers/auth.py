from fastapi import APIRouter

router = APIRouter()


@router.post("/login")
def login():
    return {"data": "login"}


@router.post("/signup")
def signup():
    return {"data": "signup"}
