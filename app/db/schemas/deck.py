from pydantic import BaseModel


class DeckIn(BaseModel):
    title: str
    description: str | None = None


class DeckOut(BaseModel):
    id: int
    title: str
    description: str | None = None
