from app.core.config import Settings


def test_proxy_url_disabled_by_default(monkeypatch):
    monkeypatch.delenv("ENABLE_PROXY", raising=False)
    monkeypatch.delenv("PROXY_HOST", raising=False)

    settings = Settings()

    assert settings.proxy_url == ""


def test_proxy_url_includes_credentials(monkeypatch):
    monkeypatch.setenv("ENABLE_PROXY", "true")
    monkeypatch.setenv("PROXY_TYPE", "http")
    monkeypatch.setenv("PROXY_HOST", "proxy.example")
    monkeypatch.setenv("PROXY_PORT", "8080")
    monkeypatch.setenv("PROXY_USERNAME", "user")
    monkeypatch.setenv("PROXY_PASSWORD", "pass")

    settings = Settings()

    assert settings.proxy_url == "http://user:pass@proxy.example:8080"


def test_webshare_proxy_enabled_requires_username_and_password(monkeypatch):
    monkeypatch.setenv("WEBSHARE_PROXY_USERNAME", "user")
    monkeypatch.setenv("WEBSHARE_PROXY_PASSWORD", "pass")
    monkeypatch.setenv("WEBSHARE_PROXY_LOCATIONS", "us,de")

    settings = Settings()

    assert settings.webshare_proxy_enabled is True
    assert settings.WEBSHARE_PROXY_LOCATIONS == ["us", "de"]
