from typing import List

from fastapi import APIRouter, Depends

from app.schemas.quiz import QuizGenerationRequest, QuizGenerationResponse, QuizAttemptCreate, QuizAttemptResponse
from app.services import wikipedia_service, llm_gemini_service
from app.api.v1.routes_auth import get_current_active_user

router = APIRouter(prefix="/quiz", tags=["quiz"])


@router.post("/generate", response_model=QuizGenerationResponse, summary="Generate quiz via Gemini")
async def generate_quiz(
    payload: QuizGenerationRequest,
    current_user = Depends(get_current_active_user),
):
    """Generate a quiz for a Wikipedia article URL using Gemini.

    We fetch the article sections directly from Wikipedia via URL,
    clean the text, and then ask Gemini to produce a JSON quiz
    (MCQs + short open questions with correct answers).
    """

    article_data = wikipedia_service.fetch_article_sections(str(payload.url))
    sections = article_data.get("sections", {}) or {}

    full_text_parts: List[str] = []
    for section_text in sections.values():
        if section_text:
            full_text_parts.append(section_text)

    full_text = "\n\n".join(full_text_parts)
    cleaned_text = wikipedia_service.clean_wikipedia_text(full_text)

    quiz_json = llm_gemini_service.generate_quiz(cleaned_text)

    return QuizGenerationResponse(
        url=payload.url,
        multiple_choice=quiz_json.get("multiple_choice", []),
        open_questions=quiz_json.get("open_questions", []),
    )


@router.post("/attempt", response_model=QuizAttemptResponse, summary="Submit quiz attempt and compute score")
async def submit_quiz_attempt(
    payload: QuizAttemptCreate,
    current_user = Depends(get_current_active_user),
):
    # TODO: persist attempt in database and return score
    raise NotImplementedError
