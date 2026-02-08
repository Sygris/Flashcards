from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.db.utils.init_db import create_tables
from app.routers.auth import router as authRouter
from app.routers.user import router as userRouter


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting API...")
    create_tables()
    print("Database has been initialised!")
    print("API has been initialised")
    yield
    print("Closing API...")


app = FastAPI(lifespan=lifespan)
app.include_router(authRouter, prefix="/auth", tags=["auth"])
app.include_router(userRouter, prefix="/user", tags=["user"])


@app.get("/health")
def health():
    return {"status": "ok"}
