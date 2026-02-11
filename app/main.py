from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.db.utils.init_db import create_tables
from app.routers.auth import router as authRouter
from app.routers.user import router as userRouter
from app.routers.deck import router as deckRouter


# Controls the life cycle of the app
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Beginning of the application
    print("Starting API...")
    create_tables()
    print("Database has been initialised!")
    yield
    # End of the application
    print("Closing API...")


# Create the application
app = FastAPI(lifespan=lifespan)

# Add the routers to the application
app.include_router(authRouter, prefix="/auth", tags=["auth"])
app.include_router(userRouter, prefix="/user", tags=["user"])
app.include_router(deckRouter, prefix="/deck", tags=["deck"])


# Endpoint used to just check if its running
@app.get("/health")
def health():
    return {"status": "ok"}
