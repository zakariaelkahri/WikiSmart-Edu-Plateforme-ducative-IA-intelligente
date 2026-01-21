from fastapi import APIRouter

from app.schemas.quiz import QuizGenerationRequest, QuizGenerationResponse, QuizAttemptCreate, QuizAttemptResponse

router = APIRouter(prefix="/quiz", tags=["quiz"])


@router.post("/generate", response_model=QuizGenerationResponse, summary="Generate quiz via Gemini")
async def generate_quiz(payload: QuizGenerationRequest):
    # TODO: call llm_gemini_service to generate quiz JSON
    raise NotImplementedError


@router.post("/attempt", response_model=QuizAttemptResponse, summary="Submit quiz attempt and compute score")
async def submit_quiz_attempt(payload: QuizAttemptCreate):
    # TODO: persist attempt in database and return score
    raise NotImplementedError
