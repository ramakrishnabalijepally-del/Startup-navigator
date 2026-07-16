import pytest

REGISTER_URL = "/auth/register"
LOGIN_URL = "/auth/login"
ARTICLES_URL = "/articles"


def _make_admin(client, db):
    """Ensure an admin user exists, then log in as that user."""
    from app.models.user import User, UserRole
    from app.services.auth_service import hash_password

    if not db.query(User).filter(User.email == "articleadmin@test.com").first():
        admin = User(
            email="articleadmin@test.com",
            hashed_password=hash_password("AdminPass123"),
            role=UserRole.admin,
        )
        db.add(admin)
        db.commit()

    client.post(LOGIN_URL, json={"email": "articleadmin@test.com", "password": "AdminPass123"})


def _make_user(client):
    client.post(REGISTER_URL, json={"email": "articleuser@test.com", "password": "UserPass123"})
    client.post(LOGIN_URL, json={"email": "articleuser@test.com", "password": "UserPass123"})


SAMPLE_ARTICLE = {
    "title": "Test Article: Company Registration",
    "category": "Registration",
    "content": "This is a detailed article about company registration steps in India.",
    "summary": "Quick guide to registration.",
    "tags": ["registration", "test"],
}


def test_list_articles_public(client):
    res = client.get(ARTICLES_URL)
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_create_article_as_admin(client, db):
    _make_admin(client, db)
    res = client.post(ARTICLES_URL, json=SAMPLE_ARTICLE)
    assert res.status_code == 201
    data = res.json()
    assert data["title"] == SAMPLE_ARTICLE["title"]
    assert data["category"] == "Registration"


def test_create_article_as_regular_user_forbidden(client):
    _make_user(client)
    res = client.post(ARTICLES_URL, json=SAMPLE_ARTICLE)
    assert res.status_code == 403


def test_create_article_unauthenticated(client):
    client.cookies.clear()
    res = client.post(ARTICLES_URL, json=SAMPLE_ARTICLE)
    assert res.status_code == 401


def test_get_article_by_id(client, db):
    _make_admin(client, db)
    create_res = client.post(ARTICLES_URL, json=SAMPLE_ARTICLE)
    article_id = create_res.json()["id"]
    res = client.get(f"{ARTICLES_URL}/{article_id}")
    assert res.status_code == 200
    assert res.json()["id"] == article_id


def test_update_article(client, db):
    _make_admin(client, db)
    create_res = client.post(ARTICLES_URL, json=SAMPLE_ARTICLE)
    article_id = create_res.json()["id"]
    res = client.put(f"{ARTICLES_URL}/{article_id}", json={"title": "Updated Title"})
    assert res.status_code == 200
    assert res.json()["title"] == "Updated Title"


def test_delete_article(client, db):
    _make_admin(client, db)
    create_res = client.post(ARTICLES_URL, json=SAMPLE_ARTICLE)
    article_id = create_res.json()["id"]
    del_res = client.delete(f"{ARTICLES_URL}/{article_id}")
    assert del_res.status_code == 204
    get_res = client.get(f"{ARTICLES_URL}/{article_id}")
    assert get_res.status_code == 404


def test_filter_articles_by_category(client, db):
    _make_admin(client, db)
    client.post(ARTICLES_URL, json={**SAMPLE_ARTICLE, "category": "Funding"})
    res = client.get(f"{ARTICLES_URL}?category=Funding")
    assert res.status_code == 200
    results = res.json()
    assert all(a["category"] == "Funding" for a in results)
