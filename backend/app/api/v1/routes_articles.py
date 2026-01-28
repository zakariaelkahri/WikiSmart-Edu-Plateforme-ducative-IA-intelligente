from typing import List

from fastapi import APIRouter, UploadFile, File, Depends

from app.schemas.article import (
    ArticleIngestRequest,
    ArticleResponse,
    SummaryRequest,
    SummaryResponse,
    TranslationRequest,
    TranslationResponse,
    WikipediaSummaryRequest,
    WikipediaSummaryResponse,
    WikipediaTranslationRequest,
    WikipediaTranslationResponse,
)
from app.services import wikipedia_service, llm_groq_service, llm_gemini_service
from app.db.session import SessionLocal
from app.models.article import Article
from fastapi import HTTPException, status
from app.api.v1.routes_auth import get_current_active_user

router = APIRouter(prefix="/articles", tags=["articles"])


@router.post("/ingest/url", response_model=ArticleResponse, summary="Ingest article from Wikipedia URL")
async def ingest_article_from_url(
    payload: ArticleIngestRequest,
    current_user = Depends(get_current_active_user),
):
    # TODO: call wikipedia_service to fetch and preprocess article
    raise NotImplementedError


@router.post("/ingest/pdf", response_model=ArticleResponse, summary="Ingest article from PDF upload")
async def ingest_article_from_pdf(
    file: UploadFile = File(...),
    current_user = Depends(get_current_active_user),
):
    # TODO: call pdf_service to extract text and preprocess
    raise NotImplementedError


@router.post("/summary", response_model=SummaryResponse, summary="Generate summary via Groq")
async def summarize_article(
    payload: SummaryRequest,
    current_user = Depends(get_current_active_user),
):
    # TODO: call llm_groq_service to summarize
    raise NotImplementedError


@router.post(
    "/summary/url",
    response_model=WikipediaSummaryResponse,
    summary="Generate article summary from Wikipedia URL via Groq",
)
async def summarize_wikipedia_article(payload: WikipediaSummaryRequest) -> WikipediaSummaryResponse:
    """Return a cleaned, LLM-generated summary of a Wikipedia article.

    This endpoint:
    - fetches the article sections from Wikipedia
    - concatenates and lightly cleans the text
    - calls Groq LLM to generate a concise summary
    """
    
    article_data = wikipedia_service.fetch_article_sections(str(payload.url))
    sections = article_data.get("sections", {}) or {}

    full_text_parts: List[str] = []
    for section_text in sections.values():
        if section_text:
            full_text_parts.append(section_text)

    full_text = "\n\n".join(full_text_parts)
    cleaned_text = wikipedia_service.clean_wikipedia_text(full_text)

    llm_result = llm_groq_service.summarize_article(cleaned_text, length=payload.length)

    return WikipediaSummaryResponse(
        url=payload.url,
        title=article_data.get("title", ""),
        length=payload.length,
        summary=llm_result.get("summary", ""),
    )


@router.post("/translate", response_model=TranslationResponse, summary="Translate article via Gemini")
async def translate_article(payload: TranslationRequest):
    """Translate an article referenced in the DB using its Wikipedia URL.

    For now we ignore processed_content_path and re-fetch the article
    directly from Wikipedia, so this works with the seeded data even
    if no local processed files exist.
    """

    db = SessionLocal()
    try:
        article: Article | None = db.query(Article).filter(Article.id == payload.article_id).first()
        if not article:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

        # Fetch and aggregate article text from Wikipedia using the stored title
        # (avoids URL parsing issues like malformed slugs)
        article_data = wikipedia_service.fetch_article_sections_by_title(article.title)
        sections = article_data.get("sections", {}) or {}

        full_text_parts: List[str] = []
        for section_text in sections.values():
            if section_text:
                full_text_parts.append(section_text)

        full_text = "\n\n".join(full_text_parts)
        cleaned_text = wikipedia_service.clean_wikipedia_text(full_text)

        translated = llm_gemini_service.translate_content(cleaned_text, payload.target_language)

        return TranslationResponse(
            article_id=payload.article_id,
            target_language=payload.target_language,
            translated_text=translated,
        )
    finally:
        db.close()


@router.post(
    "/translate/url",
    response_model=WikipediaTranslationResponse,
    summary="Translate Wikipedia article via Gemini from URL",
)
async def translate_wikipedia_article(
    payload: WikipediaTranslationRequest,
    current_user = Depends(get_current_active_user),
) -> WikipediaTranslationResponse:
    """Translate a Wikipedia article given its URL using Gemini LLM.

    This endpoint:
    - fetches the article sections from Wikipedia via URL
    - concatenates and cleans the text
    - calls Gemini to translate into the requested language
    """

    article_data = wikipedia_service.fetch_article_sections(str(payload.url))
    sections = article_data.get("sections", {}) or {}

    full_text_parts: List[str] = []
    for section_text in sections.values():
        if section_text:
            full_text_parts.append(section_text)

    full_text = "\n\n".join(full_text_parts)
    cleaned_text = wikipedia_service.clean_wikipedia_text(full_text)

    translated = llm_gemini_service.translate_content(cleaned_text, payload.target_language)

    return WikipediaTranslationResponse(
        url=payload.url,
        title=article_data.get("title", ""),
        target_language=payload.target_language,
        translated_text=translated,
    )



