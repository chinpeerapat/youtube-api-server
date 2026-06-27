from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader, HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import settings

security_bearer = HTTPBearer(auto_error=False)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token for clients using JWT auth."""
    if not settings.JWT_SECRET_KEY:
        raise HTTPException(status_code=500, detail="JWT secret key is not configured")

    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def verify_token(token: str) -> dict:
    if not settings.JWT_SECRET_KEY:
        raise HTTPException(status_code=500, detail="JWT secret key is not configured")

    try:
        return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=401, detail="Invalid token") from exc


def verify_api_key(api_key: str) -> bool:
    return bool(settings.API_KEY and api_key == settings.API_KEY)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security_bearer),
    api_key: Optional[str] = Security(api_key_header),
) -> dict:
    """Return auth context, enforcing auth only when ENABLE_AUTH is true."""
    if not settings.ENABLE_AUTH:
        return {"authenticated": True, "auth_type": "disabled"}

    if settings.AUTH_TYPE == "api_key":
        if not api_key:
            raise HTTPException(status_code=401, detail="API key required")
        if not verify_api_key(api_key):
            raise HTTPException(status_code=401, detail="Invalid API key")
        return {"authenticated": True, "auth_type": "api_key"}

    if settings.AUTH_TYPE == "jwt":
        if not credentials:
            raise HTTPException(status_code=401, detail="Token required")
        payload = verify_token(credentials.credentials)
        return {"authenticated": True, "auth_type": "jwt", "user": payload}

    raise HTTPException(status_code=500, detail="Unknown authentication type")
