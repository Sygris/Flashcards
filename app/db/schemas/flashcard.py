from pydantic import BaseModel


class FlashcardInCreate(BaseModel):
    question: str
    answer: str


class FlashcardOut(BaseModel):
    id: int
    question: str
    answer: str


class FlashcardInUpdate(BaseModel):
    question: str | None = None
    answer: str | None = None
