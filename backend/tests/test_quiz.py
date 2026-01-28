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
            "History": "Python was created by Guido van Rossum in 1991.",
        },
    }


@pytest.fixture
def mock_quiz_data():
    return {
        "multiple_choice": [
            {
                "question": "Who created Python?",
                "options": ["Guido van Rossum", "Dennis Ritchie", "Bjarne Stroustrup", "James Gosling"],
                "correct_index": 0,
            },
            {
                "question": "What type of language is Python?",
                "options": ["Low-level", "High-level", "Assembly", "Machine"],
                "correct_index": 1,
            },
        ],
        "open_questions": [
            {"question": "What is Python used for?", "answer": "Various applications including web development, data science, and automation."}
        ],
    }


class TestQuizGeneration:
    @patch("app.services.llm_gemini_service.generate_quiz")
    @patch("app.services.wikipedia_service.clean_wikipedia_text")
    @patch("app.services.wikipedia_service.fetch_article_sections")
    def test_generate_quiz_success(
        self, mock_fetch, mock_clean, mock_generate, mock_auth_user, mock_wikipedia_data, mock_quiz_data
    ):
        mock_fetch.return_value = mock_wikipedia_data
        mock_clean.return_value = "Cleaned text content"
        mock_generate.return_value = mock_quiz_data

        response = client.post(
            "/api/v1/quiz/generate",
            json={"url": "https://en.wikipedia.org/wiki/Python_(programming_language)"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "multiple_choice" in data
        assert "open_questions" in data
        assert len(data["multiple_choice"]) == 2
        assert len(data["open_questions"]) == 1
        assert data["multiple_choice"][0]["question"] == "Who created Python?"
        mock_fetch.assert_called_once()
        mock_generate.assert_called_once()

    def test_generate_quiz_invalid_url(self, mock_auth_user):
        response = client.post(
            "/api/v1/quiz/generate",
            json={"url": "invalid-url"},
        )
        assert response.status_code == 422  # Validation error

    def test_generate_quiz_without_auth(self):
        with patch("app.api.v1.routes_auth.get_current_active_user", side_effect=Exception("Not authenticated")):
            response = client.post(
                "/api/v1/quiz/generate",
                json={"url": "https://en.wikipedia.org/wiki/Test"},
            )
            assert response.status_code in [401, 500]


class TestQuizAttempt:
    def test_submit_quiz_attempt_not_implemented(self, mock_auth_user):
        response = client.post(
            "/api/v1/quiz/attempt",
            json={"article_id": 1, "answers_mcq": {0: 0, 1: 1}, "answers_open": {0: "test answer"}},
        )
        # Endpoint returns 500 with NotImplementedError
        assert response.status_code == 500
