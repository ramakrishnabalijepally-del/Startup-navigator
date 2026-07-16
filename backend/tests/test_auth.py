import pytest


REGISTER_URL = "/auth/register"
LOGIN_URL = "/auth/login"
ME_URL = "/auth/me"
LOGOUT_URL = "/auth/logout"


def test_register_success(client):
    res = client.post(REGISTER_URL, json={
        "email": "newuser@test.com",
        "password": "Password123",
        "full_name": "New User",
    })
    assert res.status_code == 201
    data = res.json()
    assert data["user"]["email"] == "newuser@test.com"
    assert data["user"]["role"] == "user"
    assert "access_token" in data
    # httpOnly cookie should be set
    assert "access_token" in res.cookies


def test_register_duplicate_email(client):
    payload = {"email": "dup@test.com", "password": "Password123"}
    client.post(REGISTER_URL, json=payload)
    res = client.post(REGISTER_URL, json=payload)
    assert res.status_code == 400
    assert "already registered" in res.json()["detail"]


def test_register_weak_password(client):
    res = client.post(REGISTER_URL, json={"email": "weak@test.com", "password": "123"})
    assert res.status_code == 422


def test_login_success(client):
    client.post(REGISTER_URL, json={"email": "login@test.com", "password": "Password123"})
    res = client.post(LOGIN_URL, json={"email": "login@test.com", "password": "Password123"})
    assert res.status_code == 200
    assert res.json()["user"]["email"] == "login@test.com"
    assert "access_token" in res.cookies


def test_login_wrong_password(client):
    client.post(REGISTER_URL, json={"email": "wrongpw@test.com", "password": "Password123"})
    res = client.post(LOGIN_URL, json={"email": "wrongpw@test.com", "password": "wrong"})
    assert res.status_code == 401


def test_login_unknown_email(client):
    res = client.post(LOGIN_URL, json={"email": "nobody@test.com", "password": "Password123"})
    assert res.status_code == 401


def test_me_authenticated(client):
    client.post(REGISTER_URL, json={"email": "me@test.com", "password": "Password123"})
    client.post(LOGIN_URL, json={"email": "me@test.com", "password": "Password123"})
    res = client.get(ME_URL)
    assert res.status_code == 200
    assert res.json()["email"] == "me@test.com"


def test_me_unauthenticated(client):
    res = client.get(ME_URL)
    assert res.status_code == 401


def test_logout(client):
    client.post(REGISTER_URL, json={"email": "logout@test.com", "password": "Password123"})
    client.post(LOGIN_URL, json={"email": "logout@test.com", "password": "Password123"})
    res = client.post(LOGOUT_URL)
    assert res.status_code == 200
    # After logout, /me should return 401
    res2 = client.get(ME_URL)
    assert res2.status_code == 401
