from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.utils.init_db import create_tables
from app.routers.auth import router as authRouter


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


@app.get("/health")
def health():
    return {"status": "ok"}
