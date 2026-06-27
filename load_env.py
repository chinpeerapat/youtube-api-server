#!/usr/bin/env python3
"""Environment configuration checker for the YouTube API server."""

from app.core.config import settings


def _status(name: str, value: object, required: bool = False) -> str:
    marker = "OK" if value else ("MISSING" if required else "unset")
    return f"{name}: {marker}"


def load_env_file() -> None:
    print("Server")
    print(_status("HOST", settings.HOST, True))
    print(_status("PORT", settings.PORT, True))
    print(_status("LOG_LEVEL", settings.LOG_LEVEL, True))

    print("\nGeneric proxy")
    print(_status("ENABLE_PROXY", settings.ENABLE_PROXY))
    print(_status("PROXY_HOST", settings.PROXY_HOST, settings.ENABLE_PROXY))
    print(_status("PROXY_PORT", settings.PROXY_PORT, settings.ENABLE_PROXY))
    print(f"proxy_url: {'configured' if settings.proxy_url else 'disabled'}")

    print("\nWebshare transcript proxy")
    print(_status("WEBSHARE_PROXY_USERNAME", settings.WEBSHARE_PROXY_USERNAME))
    print(_status("WEBSHARE_PROXY_PASSWORD", settings.WEBSHARE_PROXY_PASSWORD))
    print(f"WEBSHARE_PROXY_LOCATIONS: {','.join(settings.WEBSHARE_PROXY_LOCATIONS)}")
    print(f"webshare_proxy: {'enabled' if settings.webshare_proxy_enabled else 'disabled'}")

    print("\nAuthentication")
    print(_status("ENABLE_AUTH", settings.ENABLE_AUTH))
    print(f"AUTH_TYPE: {settings.AUTH_TYPE}")
    print(_status("API_KEY", settings.API_KEY, settings.ENABLE_AUTH and settings.AUTH_TYPE == "api_key"))
    print(_status("JWT_SECRET_KEY", settings.JWT_SECRET_KEY, settings.ENABLE_AUTH and settings.AUTH_TYPE == "jwt"))


if __name__ == "__main__":
    load_env_file()
