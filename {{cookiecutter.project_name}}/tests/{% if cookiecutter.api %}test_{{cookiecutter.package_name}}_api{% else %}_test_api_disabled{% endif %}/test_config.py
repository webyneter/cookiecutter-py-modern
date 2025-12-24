"""API configuration tests."""

import pytest

from {{cookiecutter.package_name}}_api.config import Settings


def test_settings_default_values(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test default settings values."""
    # Clear environment variables to test actual defaults
    monkeypatch.delenv("DEBUG", raising=False)
    monkeypatch.delenv("ENVIRONMENT", raising=False)
    monkeypatch.delenv("HOST", raising=False)
    monkeypatch.delenv("PORT", raising=False)

    settings = Settings()

    assert settings.debug is False
    assert settings.environment == "development"
    assert settings.host == "0.0.0.0"
    assert settings.port == 8000


def test_settings_cors_origins_default() -> None:
    """Test default CORS origins."""
    settings = Settings()

    assert isinstance(settings.cors_origins, list)
    assert "http://localhost:3000" in settings.cors_origins


def test_settings_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test settings loaded from environment variables."""
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("PORT", "9000")

    settings = Settings()

    assert settings.debug is True
    assert settings.environment == "production"
    assert settings.port == 9000
