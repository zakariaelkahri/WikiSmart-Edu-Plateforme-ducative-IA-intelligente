from typing import Dict, Any

from google import genai

from app.core.config import settings


_client: genai.Client | None = None


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        if not settings.gemini_api_key:
            raise RuntimeError("Gemini API key is not configured")
        _client = genai.Client(api_key=settings.gemini_api_key)
    return _client


def translate_content(content: str, target_language: str) -> str:
    """Translate arbitrary text into the requested language using Gemini.

    target_language is expected to be a short code like "EN", "FR", "ES", etc.
    """

    if not content:
        return ""

    # Basic normalization of language code
    target_language = (target_language or "").strip()
    if not target_language:
        raise ValueError("target_language is required")

    # Truncate long inputs to stay within model limits
    if len(content) > settings.llm_max_input_chars:
        content = content[: settings.llm_max_input_chars]

    client = _get_client()

    system_instruction = (
        "You are a translation assistant for an educational platform. "
        "Translate the given text into the target language while preserving meaning "
        "and keeping a neutral, clear tone. Return only the translated text."
    )

    prompt = (
        f"{system_instruction}\n\n"
        f"Target language: {target_language}.\n"
        f"Text to translate:\n{content}"
    )

    # Pass a single string as contents to satisfy google-genai's
    # _GenerateContentParameters schema and avoid Pydantic validation errors.
    response = client.models.generate_content(
        model=settings.gemini_model_name_translation,
        contents=prompt,
    )

    # google-genai responses expose .text for the main content
    translated_text = getattr(response, "text", None)
    if not translated_text and getattr(response, "candidates", None):
        # Fallback extraction for older/newer response shapes
        try:
            translated_text = response.candidates[0].content.parts[0].text
        except Exception:  # noqa: BLE001
            translated_text = ""
    return translated_text or ""


def generate_quiz(content: str) -> Dict[str, Any]:
    # TODO: integrate Google Gemini for quiz generation with strict JSON schema
    raise NotImplementedError
