from datetime import datetime
from typing import List, Dict, Any

from pydantic import BaseModel


class MultipleChoiceQuestion(BaseModel):
    question: str
    options: List[str]
    correct_index: int


class OpenQuestion(BaseModel):
    question: str
    answer: str


class QuizGenerationRequest(BaseModel):
    article_id: int


class QuizGenerationResponse(BaseModel):
    article_id: int
    multiple_choice: List[MultipleChoiceQuestion]
    open_questions: List[OpenQuestion]


class QuizAttemptCreate(BaseModel):
    article_id: int
    answers_mcq: Dict[int, int]  # question index -> selected option index
    answers_open: Dict[int, str]  # question index -> user free-text answer


class QuizAttemptResponse(BaseModel):
    attempt_id: int
    score: float


class QuizAttemptDB(BaseModel):
    id: int
    userid: int
    articleid: int
    score: float
    submittedat: datetime | None = None

    class Config:
        from_attributes = True
