"""
Shared test fixtures and configuration for pytest
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from app.main import app


@pytest.fixture(scope="module")
def test_client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def sample_wikipedia_article():
    """Sample Wikipedia article data for testing"""
    return {
        "title": "Artificial Intelligence",
        "url": "https://en.wikipedia.org/wiki/Artificial_Intelligence",
        "sections": {
            "Introduction": "Artificial intelligence (AI) is intelligence demonstrated by machines.",
            "History": "The field of AI research was founded at a workshop at Dartmouth College in 1956.",
            "Applications": "AI is used in various fields including healthcare, finance, and transportation.",
        },
    }


@pytest.fixture
def sample_user_credentials():
    """Sample user credentials for testing"""
    return {"username": "testuser", "password": "testpass123", "email": "test@example.com"}


@pytest.fixture
def sample_quiz():
    """Sample quiz data for testing"""
    return {
        "multiple_choice": [
            {
                "question": "What does AI stand for?",
                "options": ["Artificial Intelligence", "Automated Information", "Applied Integration", "Advanced Iteration"],
                "correct_index": 0,
            }
        ],
        "open_questions": [{"question": "Explain the concept of machine learning.", "answer": "Machine learning is a subset of AI that enables systems to learn from data."}],
    }
