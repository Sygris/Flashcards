from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.auth import router as authRouter
from app.routers.user import router as userRouter
from app.routers.deck import router as deckRouter
from app.routers.flashcard import router as flashcardRouter


# Create the application
app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add the routers to the application
app.include_router(authRouter, prefix="/auth", tags=["auth"])
app.include_router(userRouter, prefix="/user", tags=["user"])
app.include_router(deckRouter, prefix="/decks", tags=["deck"])
app.include_router(
    flashcardRouter, prefix="/decks/{deck_id}/flashcards", tags=["flashcard"]
)


# Endpoint used to just check if its running
@app.get("/health")
def health():
    return {"status": "ok"}
