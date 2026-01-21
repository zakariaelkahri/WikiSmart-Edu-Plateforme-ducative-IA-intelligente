from datetime import datetime
from typing import Dict, Any

from pydantic import BaseModel, HttpUrl


class ArticleIngestRequest(BaseModel):
    url: HttpUrl


class ArticleResponse(BaseModel):
    id: int
    url: str
    title: str
    action: str
    createdat: datetime | None = None
    metadata: Dict[str, Any] | None = None

    class Config:
        from_attributes = True


class SummaryRequest(BaseModel):
    article_id: int
    length: str = "medium"  # short | medium


class SummaryResponse(BaseModel):
    article_id: int
    summary: str


class WikipediaSummaryRequest(BaseModel):
    url: HttpUrl
    length: str = "medium"  # short | medium


class WikipediaSummaryResponse(BaseModel):
    url: HttpUrl
    title: str
    length: str
    summary: str


class TranslationRequest(BaseModel):
    article_id: int
    target_language: str  # FR, EN, AR, ES, etc.


class TranslationResponse(BaseModel):
    article_id: int
    target_language: str
    translated_text: str


class WikipediaTranslationRequest(BaseModel):
    url: HttpUrl
    target_language: str  # FR, EN, AR, ES, etc.


class WikipediaTranslationResponse(BaseModel):
    url: HttpUrl
    title: str
    target_language: str
    translated_text: str
