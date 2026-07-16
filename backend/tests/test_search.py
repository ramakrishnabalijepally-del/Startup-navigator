"""
Search endpoint tests — RAG calls to Gemini are mocked.
"""
import pytest
from unittest.mock import patch, MagicMock

REGISTER_URL = "/auth/register"
LOGIN_URL = "/auth/login"
SEARCH_URL = "/search"

MOCK_RAG_RESULT = {
    "answer": "To register a company in India, you need to obtain a DSC, DIN, and file the SPICe+ form.",
    "sources": [
        {"article_id": 1, "title": "Company Registration Guide", "category": "Registration", "excerpt": "Step 1..."},
    ],
    "category_hint": "Registration",
}


def _login_user(client):
    client.post(REGISTER_URL, json={"email": "searchuser@test.com", "password": "Password123"})
    client.post(LOGIN_URL, json={"email": "searchuser@test.com", "password": "Password123"})


def test_search_requires_auth(client):
    client.cookies.clear()
    res = client.post(SEARCH_URL, json={"query": "how to register a company"})
    assert res.status_code == 401


def test_search_empty_query(client):
    _login_user(client)
    res = client.post(SEARCH_URL, json={"query": "   "})
    assert res.status_code == 400


def test_search_success_mocked(client):
    _login_user(client)

    mock_rag = MagicMock()
    mock_rag.search.return_value = MOCK_RAG_RESULT

    with patch("app.routers.search.get_rag_service", return_value=mock_rag):
        res = client.post(SEARCH_URL, json={"query": "how to register a company in India"})

    assert res.status_code == 200
    data = res.json()
    assert data["answer"] == MOCK_RAG_RESULT["answer"]
    assert len(data["sources"]) == 1
    assert data["sources"][0]["category"] == "Registration"
    assert "history_id" in data


def test_search_stores_history(client, db):
    _login_user(client)
    from app.models.search_history import SearchHistory

    mock_rag = MagicMock()
    mock_rag.search.return_value = MOCK_RAG_RESULT

    with patch("app.routers.search.get_rag_service", return_value=mock_rag):
        res = client.post(SEARCH_URL, json={"query": "what is DPIIT recognition"})

    assert res.status_code == 200
    history_id = res.json()["history_id"]
    entry = db.query(SearchHistory).filter(SearchHistory.id == history_id).first()
    assert entry is not None
    assert entry.query == "what is DPIIT recognition"
    assert entry.category_hint == "Registration"


def test_search_rag_error_returns_503(client):
    _login_user(client)

    mock_rag = MagicMock()
    mock_rag.search.side_effect = Exception("Gemini API rate limit")

    with patch("app.routers.search.get_rag_service", return_value=mock_rag):
        res = client.post(SEARCH_URL, json={"query": "some query"})

    assert res.status_code == 503
    assert "temporarily unavailable" in res.json()["detail"]
