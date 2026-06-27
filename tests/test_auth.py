from datetime import timedelta

import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from app.middleware.auth import create_access_token, get_current_user


@pytest.mark.asyncio
async def test_auth_disabled_allows_request(monkeypatch):
    monkeypatch.setattr("app.middleware.auth.settings.ENABLE_AUTH", False)

    user = await get_current_user(credentials=None, api_key=None)

    assert user == {"authenticated": True, "auth_type": "disabled"}


@pytest.mark.asyncio
async def test_api_key_auth_success_and_failure(monkeypatch):
    monkeypatch.setattr("app.middleware.auth.settings.ENABLE_AUTH", True)
    monkeypatch.setattr("app.middleware.auth.settings.AUTH_TYPE", "api_key")
    monkeypatch.setattr("app.middleware.auth.settings.API_KEY", "secret")

    assert await get_current_user(credentials=None, api_key="secret") == {
        "authenticated": True,
        "auth_type": "api_key",
    }

    with pytest.raises(HTTPException) as exc:
        await get_current_user(credentials=None, api_key="wrong")
    assert exc.value.status_code == 401


@pytest.mark.asyncio
async def test_jwt_auth_success_and_failure(monkeypatch):
    monkeypatch.setattr("app.middleware.auth.settings.ENABLE_AUTH", True)
    monkeypatch.setattr("app.middleware.auth.settings.AUTH_TYPE", "jwt")
    monkeypatch.setattr("app.middleware.auth.settings.JWT_SECRET_KEY", "jwt-secret")

    token = create_access_token({"sub": "user-1"}, expires_delta=timedelta(minutes=5))
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)

    user = await get_current_user(credentials=credentials, api_key=None)

    assert user["authenticated"] is True
    assert user["auth_type"] == "jwt"
    assert user["user"]["sub"] == "user-1"

    bad_credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="bad")
    with pytest.raises(HTTPException) as exc:
        await get_current_user(credentials=bad_credentials, api_key=None)
    assert exc.value.status_code == 401
