from typing import Dict, Any
from urllib.parse import urlparse, unquote
import re

import requests
import wikipedia

from app.core.config import settings


session = requests.Session()
session.headers.update({
    "User-Agent": settings.wikipedia_user_agent,
})

wikipedia.requests = session


def extract_title_from_url(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path
    if not path:
        raise ValueError("Invalid Wikipedia URL")

    slug = path.split("/")[-1]
    slug = unquote(slug)
    title = slug.replace("_", " ")
    return title


def fetch_article_sections(url: str) -> Dict[str, Any]:
    title = extract_title_from_url(url)
    page = wikipedia.page(title)
    content = page.content

    sections: Dict[str, Any] = {}
    current_section = "Introduction"
    sections[current_section] = []

    for line in content.splitlines():
        line = line.strip()
        if line.startswith("===") and line.endswith("==="):
            section_title = line.strip("=").strip()
            current_section = section_title
            sections[current_section] = []
        elif line:
            sections[current_section].append(line)

    for key in list(sections.keys()):
        sections[key] = "\n".join(sections[key])

    return {
        "title": page.title,
        "url": page.url,
        "sections": sections,
    }


def fetch_article_sections_by_title(title: str) -> Dict[str, Any]:
    """Fetch article sections given a Wikipedia page title.

    This bypasses URL parsing and is useful when we already
    know the canonical title from the database.
    """
    page = wikipedia.page(title)
    content = page.content

    sections: Dict[str, Any] = {}
    current_section = "Introduction"
    sections[current_section] = []

    for line in content.splitlines():
        line = line.strip()
        if line.startswith("===") and line.endswith("==="):
            section_title = line.strip("=").strip()
            current_section = section_title
            sections[current_section] = []
        elif line:
            sections[current_section].append(line)

    for key in list(sections.keys()):
        sections[key] = "\n".join(sections[key])

    return {
        "title": page.title,
        "url": page.url,
        "sections": sections,
    }


def clean_wikipedia_text(text: str) -> str:
    """Lightly clean Wikipedia text for LLM consumption.

    - Remove reference markers like [1], [12]
    - Collapse excessive whitespace
    """

    # Remove numeric reference markers [1], [23], etc.
    cleaned = re.sub(r"\[\d+\]", "", text)
    # Normalize whitespace
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()
