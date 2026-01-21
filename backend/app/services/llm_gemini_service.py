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
    """Generate a quiz in strict JSON format from article content using Gemini.

    The returned dict has the shape expected by QuizGenerationResponse:
    {
      "multiple_choice": [
        {"question": str, "options": [str, str, str, str], "correct_index": int},
        ...
      ],
      "open_questions": [
        {"question": str, "answer": str},
        ...
      ],
    }
    """

    if not content:
        return {"multiple_choice": [], "open_questions": []}

    # Truncate long inputs to stay within model limits
    if len(content) > settings.llm_max_input_chars:
        content = content[: settings.llm_max_input_chars]

    client = _get_client()

    system_instruction = (
        "You are an educational quiz generator. "
        "Given article content, you produce a small quiz for students. "
        "You must respond with STRICT JSON that matches this schema exactly: \n"
        "{\n"
        "  \"multiple_choice\": [\n"
        "    {\n"
        "      \"question\": string,\n"
        "      \"options\": [string, string, string, string],\n"
        "      \"correct_index\": integer between 0 and 3\n"
        "    }, ...\n"
        "  ],\n"
        "  \"open_questions\": [\n"
        "    {\n"
        "      \"question\": string,\n"
        "      \"answer\": string\n"
        "    }, ...\n"
        "  ]\n"
        "}.\n"
        "Do not include any keys other than these, and do not include explanations."
    )

    prompt = (
        f"{system_instruction}\n\n"
        f"Article content:\n{content}"
    )

    response = client.models.generate_content(
        model=settings.gemini_model_name_quiz,
        contents=prompt,
    )

    raw = getattr(response, "text", None) or ""

    import json
    import re

    # Try direct JSON parse first
    try:
        parsed = json.loads(raw)
    except Exception:  # noqa: BLE001
        # Strip markdown code fences if present
        if "```" in raw:
            # Remove ```json or ``` and closing ```
            raw_clean = re.sub(r"```(json)?", "", raw, flags=re.IGNORECASE).strip()
        else:
            raw_clean = raw

        # Try to extract the first JSON object from the text
        match = re.search(r"\{[\s\S]*\}", raw_clean)
        if match:
            candidate = match.group(0)
            try:
                parsed = json.loads(candidate)
            except Exception:  # noqa: BLE001
                parsed = None
        else:
            parsed = None

    if not parsed or not isinstance(parsed, dict):
        # If parsing still fails, fall back to empty quiz to avoid 500s
        return {"multiple_choice": [], "open_questions": []}

    # Basic shape check; if keys missing, normalize to expected shape
    mcq = parsed.get("multiple_choice") or []
    open_q = parsed.get("open_questions") or []
    return {"multiple_choice": mcq, "open_questions": open_q}
