from typing import Dict, Any

from groq import Groq

from app.core.config import settings


_client: Groq | None = None


def _get_client() -> Groq:
    global _client
    if _client is None:
        if not settings.groq_api_key:
            raise RuntimeError("Groq API key is not configured")
        _client = Groq(api_key=settings.groq_api_key)
    return _client


def summarize_article(content: str, length: str = "medium") -> Dict[str, Any]:
    """Summarize an article's content using Groq LLM.

    Length can be "short" or "medium" (default). The model name and
    generation params come from settings.
    """

    if length not in {"short", "medium"}:
        length = "medium"

    # Truncate very long content to stay within Groq token limits.
    # This is a simple character-based heuristic to avoid 413 / rate_limit_exceeded errors.
    if len(content) > settings.llm_max_input_chars:
        content = content[: settings.llm_max_input_chars]

    client = _get_client()

    length_instruction = {
        "short": "Provide a very short summary (2-3 concise sentences).",
        "medium": "Provide a medium-length summary (1 short paragraph).",
    }[length]

    system_prompt = (
        "You are an educational assistant. You write clear, neutral, "
        "and concise summaries of educational articles for students."
    )

    user_prompt = (
        f"{length_instruction} Focus only on the core ideas, "
        f"without bullets, in plain text.\n\nArticle content:\n{content}"
    )

    completion = client.chat.completions.create(
        model=settings.groq_model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=settings.llm_temperature,
        max_tokens=settings.llm_max_tokens,
    )

    message = completion.choices[0].message.content.strip() if completion.choices else ""

    return {
        "summary": message,
        "model": settings.groq_model_name,
    }
