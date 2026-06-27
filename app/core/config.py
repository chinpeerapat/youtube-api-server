import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def _get_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}

def _get_int(name: str, default: int = 0) -> int:
    value = os.getenv(name)
    if not value:
        return default
    return int(value)

def _get_list(name: str, default: list[str] | None = None) -> list[str]:
    value = os.getenv(name)
    if not value:
        return default or []
    return [item.strip() for item in value.split(",") if item.strip()]

class Settings:
    """
    Application settings
    
    Reads settings from environment variables or .env file
    """
    def __init__(self) -> None:
        # API settings
        self.API_V1_STR: str = "/api/v1"
        self.PROJECT_NAME: str = "YouTube Tools API"

        # Server settings
        self.HOST: str = os.getenv("HOST", "0.0.0.0")
        self.PORT: int = int(os.getenv("PORT", "8000"))
        self.RELOAD: bool = _get_bool("RELOAD", False)

        # CORS settings - add specific origins in production
        self.BACKEND_CORS_ORIGINS: list[str] = _get_list("BACKEND_CORS_ORIGINS", ["*"])

        # Logging
        self.LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

        # Generic HTTP proxy settings for oEmbed/metadata calls
        self.ENABLE_PROXY: bool = _get_bool("ENABLE_PROXY", False)
        self.PROXY_TYPE: str = os.getenv("PROXY_TYPE", "http")
        self.PROXY_HOST: str = os.getenv("PROXY_HOST", "")
        self.PROXY_PORT: int = _get_int("PROXY_PORT", 0)
        self.PROXY_USERNAME: str = os.getenv("PROXY_USERNAME", "")
        self.PROXY_PASSWORD: str = os.getenv("PROXY_PASSWORD", "")

        # Webshare proxy settings for youtube-transcript-api calls
        self.WEBSHARE_PROXY_USERNAME: str = os.getenv("WEBSHARE_PROXY_USERNAME", "")
        self.WEBSHARE_PROXY_PASSWORD: str = os.getenv("WEBSHARE_PROXY_PASSWORD", "")
        self.WEBSHARE_PROXY_LOCATIONS: list[str] = _get_list("WEBSHARE_PROXY_LOCATIONS", ["de", "us"])

        # Optional authentication settings
        self.ENABLE_AUTH: bool = _get_bool("ENABLE_AUTH", False)
        self.AUTH_TYPE: str = os.getenv("AUTH_TYPE", "api_key")
        self.API_KEY: str = os.getenv("API_KEY", "")
        self.JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "")
        self.JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
        self.JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = _get_int("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 30)

    @property
    def proxy_url(self) -> str:
        """Build a generic proxy URL for HTTP metadata requests."""
        if not self.ENABLE_PROXY or not self.PROXY_HOST:
            return ""

        auth = ""
        if self.PROXY_USERNAME and self.PROXY_PASSWORD:
            auth = f"{self.PROXY_USERNAME}:{self.PROXY_PASSWORD}@"

        port = f":{self.PROXY_PORT}" if self.PROXY_PORT else ""
        return f"{self.PROXY_TYPE}://{auth}{self.PROXY_HOST}{port}"

    @property
    def webshare_proxy_enabled(self) -> bool:
        return bool(self.WEBSHARE_PROXY_USERNAME and self.WEBSHARE_PROXY_PASSWORD)

# Create settings instance
settings = Settings()
