# WikiSmart Edu - API Tests

## Overview

This directory contains comprehensive test suites for all WikiSmart Edu API endpoints.

## Test Files

- `test_health.py` - Health check endpoint tests
- `test_auth.py` - Authentication and authorization tests (register, login, JWT)
- `test_articles.py` - Article endpoints tests (summary, translation)
- `test_quiz.py` - Quiz generation and attempt tests
- `conftest.py` - Shared fixtures and test configuration

## Running Tests

### Run all tests
```bash
cd backend
pytest
```

### Run specific test file
```bash
pytest tests/test_auth.py
pytest tests/test_articles.py
pytest tests/test_quiz.py
```

### Run with coverage
```bash
pytest --cov=app --cov-report=html
```

### Run specific test function
```bash
pytest tests/test_auth.py::test_register_user
pytest tests/test_articles.py::TestSummaryEndpoint::test_summarize_wikipedia_article_success
```

### Run with verbose output
```bash
pytest -v
```

### Run only unit tests
```bash
pytest -m unit
```

## Test Coverage

The test suite covers:

1. **Authentication (`test_auth.py`)**
   - User registration with validation
   - Login with correct/incorrect credentials
   - JWT token generation
   - Duplicate username handling

2. **Article Endpoints (`test_articles.py`)**
   - Wikipedia article summarization
   - Article translation to multiple languages
   - Authentication requirements
   - Input validation

3. **Quiz Endpoints (`test_quiz.py`)**
   - Quiz generation from Wikipedia URLs
   - Multiple choice questions
   - Open-ended questions
   - Authentication requirements

4. **Health Check (`test_health.py`)**
   - Basic health endpoint verification

## Mocking Strategy

Tests use mocking to:
- Avoid calling external APIs (Wikipedia, Groq, Gemini)
- Isolate endpoint logic from service implementations
- Speed up test execution
- Ensure consistent test results

## Adding New Tests

When adding new endpoints:

1. Create test functions in the appropriate test file
2. Use fixtures from `conftest.py` for common test data
3. Mock external dependencies (Wikipedia, LLM services)
4. Test both success and error cases
5. Verify authentication requirements

## CI/CD Integration

These tests can be integrated into CI/CD pipelines:

```yaml
# Example for GitHub Actions
- name: Run tests
  run: |
    cd backend
    pytest --cov=app --cov-report=xml
```
