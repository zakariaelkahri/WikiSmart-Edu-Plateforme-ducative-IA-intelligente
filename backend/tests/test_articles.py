import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.main import app
from app.api.v1.routes_auth import get_current_active_user
from app.models.user import User, Role


client = TestClient(app)


@pytest.fixture
def mock_auth_user():
    """Mock authenticated user for protected endpoints"""
    mock_user = MagicMock(spec=User)
    mock_user.id = 1
    mock_user.username = "testuser"
    mock_user.email = "test@example.com"
    mock_user.role = Role.USER
    
    async def override_get_current_user():
        return mock_user
    
    app.dependency_overrides[get_current_active_user] = override_get_current_user
    yield mock_user
    app.dependency_overrides.clear()


@pytest.fixture
def mock_wikipedia_data():
    return {
        "title": "Python (programming language)",
        "url": "https://en.wikipedia.org/wiki/Python_(programming_language)",
        "sections": {
            "Summary": "Python is a high-level programming language.",
            "History": "Python was created by Guido van Rossum.",
        },
    }


@pytest.fixture
def mock_summary_response():
    return {"summary": "Python is a popular programming language used for various applications."}


@pytest.fixture
def mock_translation_response():
    return "Python est un langage de programmation de haut niveau."


class TestSummaryEndpoint:
    @patch("app.services.llm_groq_service.summarize_article")
    @patch("app.services.wikipedia_service.clean_wikipedia_text")
    @patch("app.services.wikipedia_service.fetch_article_sections")
    def test_summarize_wikipedia_article_success(
        self, mock_fetch, mock_clean, mock_summarize, mock_wikipedia_data, mock_summary_response
    ):
        mock_fetch.return_value = mock_wikipedia_data
        mock_clean.return_value = "Cleaned text content"
        mock_summarize.return_value = mock_summary_response

        response = client.post(
            "/api/v1/articles/summary/url",
            json={"url": "https://en.wikipedia.org/wiki/Python_(programming_language)", "length": "medium"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Python (programming language)"
        assert "summary" in data
        assert data["length"] == "medium"
        mock_fetch.assert_called_once()
        mock_summarize.assert_called_once()

    def test_summarize_wikipedia_article_invalid_url(self):
        response = client.post(
            "/api/v1/articles/summary/url",
            json={"url": "not-a-valid-url", "length": "medium"},
        )
        assert response.status_code == 422  # Validation error


class TestTranslationEndpoint:
    @patch("app.services.llm_gemini_service.translate_content")
    @patch("app.services.wikipedia_service.clean_wikipedia_text")
    @patch("app.services.wikipedia_service.fetch_article_sections")
    def test_translate_wikipedia_article_success(
        self, mock_fetch, mock_clean, mock_translate, mock_auth_user, mock_wikipedia_data, mock_translation_response
    ):
        mock_fetch.return_value = mock_wikipedia_data
        mock_clean.return_value = "Cleaned text content"
        mock_translate.return_value = mock_translation_response

        response = client.post(
            "/api/v1/articles/translate/url",
            json={"url": "https://en.wikipedia.org/wiki/Python_(programming_language)", "target_language": "FR"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Python (programming language)"
        assert data["target_language"] == "FR"
        assert "translated_text" in data
        mock_fetch.assert_called_once()
        mock_translate.assert_called_once()

    def test_translate_without_auth(self):
        with patch("app.api.v1.routes_auth.get_current_active_user", side_effect=Exception("Not authenticated")):
            response = client.post(
                "/api/v1/articles/translate/url",
                json={"url": "https://en.wikipedia.org/wiki/Test", "target_language": "FR"},
            )
            assert response.status_code in [401, 500]  # Authentication error
