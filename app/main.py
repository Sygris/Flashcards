from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db.init_db import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting API...")
    create_tables()
    print("Database has been initialised!")
    print("API has been initialised")
    yield
    print("Closing API...")


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}
