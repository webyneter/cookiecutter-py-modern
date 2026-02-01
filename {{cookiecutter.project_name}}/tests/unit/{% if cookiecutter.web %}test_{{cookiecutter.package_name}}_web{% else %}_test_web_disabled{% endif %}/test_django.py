"""Tests for Django web application."""

import os

import pytest

# Set Django settings module before importing Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{{cookiecutter.package_name}}_web.settings")


class TestDjangoSettings:
    """Tests for Django settings configuration."""

    def test_settings_can_be_imported(self) -> None:
        """Django settings should be importable."""
        from {{cookiecutter.package_name}}_web import settings

        assert settings is not None

    def test_secret_key_configured(self) -> None:
        """SECRET_KEY should be configured."""
        from {{cookiecutter.package_name}}_web.settings import SECRET_KEY

        assert SECRET_KEY is not None
        assert len(SECRET_KEY) > 0

    def test_installed_apps_configured(self) -> None:
        """INSTALLED_APPS should contain required apps."""
        from {{cookiecutter.package_name}}_web.settings import INSTALLED_APPS

        assert "django.contrib.admin" in INSTALLED_APPS
        assert "django.contrib.auth" in INSTALLED_APPS
        assert "health_check" in INSTALLED_APPS

    def test_middleware_configured(self) -> None:
        """MIDDLEWARE should contain security middleware."""
        from {{cookiecutter.package_name}}_web.settings import MIDDLEWARE

        assert "django.middleware.security.SecurityMiddleware" in MIDDLEWARE
        assert "csp.middleware.CSPMiddleware" in MIDDLEWARE

    def test_database_configured(self) -> None:
        """DATABASES should have a default configuration."""
        from {{cookiecutter.package_name}}_web.settings import DATABASES

        assert "default" in DATABASES
        assert "ENGINE" in DATABASES["default"]

    def test_argon2_password_hasher_configured(self) -> None:
        """Argon2 should be the primary password hasher."""
        from {{cookiecutter.package_name}}_web.settings import PASSWORD_HASHERS

        assert PASSWORD_HASHERS[0] == "django.contrib.auth.hashers.Argon2PasswordHasher"

    def test_csp_configured(self) -> None:
        """CSP settings should be configured."""
        from {{cookiecutter.package_name}}_web.settings import CSP_DEFAULT_SRC

        assert CSP_DEFAULT_SRC is not None


class TestWSGIApplication:
    """Tests for WSGI application."""

    def test_wsgi_application_can_be_imported(self) -> None:
        """WSGI application should be importable."""
        from {{cookiecutter.package_name}}_web.wsgi import application

        assert application is not None

    def test_wsgi_application_is_callable(self) -> None:
        """WSGI application should be callable."""
        from {{cookiecutter.package_name}}_web.wsgi import application

        assert callable(application)


class TestASGIApplication:
    """Tests for ASGI application."""

    def test_asgi_application_can_be_imported(self) -> None:
        """ASGI application should be importable."""
        from {{cookiecutter.package_name}}_web.asgi import application

        assert application is not None

    def test_asgi_application_is_callable(self) -> None:
        """ASGI application should be callable."""
        from {{cookiecutter.package_name}}_web.asgi import application

        assert callable(application)


class TestURLConfiguration:
    """Tests for URL configuration."""

    def test_urls_can_be_imported(self) -> None:
        """URL configuration should be importable."""
        import django

        django.setup()
        from {{cookiecutter.package_name}}_web import urls

        assert urls is not None

    def test_urlpatterns_defined(self) -> None:
        """urlpatterns should be defined."""
        import django

        django.setup()
        from {{cookiecutter.package_name}}_web.urls import urlpatterns

        assert urlpatterns is not None
        assert len(urlpatterns) > 0


@pytest.mark.django_db
class TestDjangoIntegration:
    """Integration tests for Django application."""

    def test_django_check_passes(self) -> None:
        """Django system check should pass."""
        import django
        from django.core.management import call_command

        django.setup()

        # This will raise an exception if checks fail
        call_command("check", verbosity=0)

    def test_admin_site_accessible(self) -> None:
        """Admin site should be configured."""
        from django.contrib import admin

        assert admin.site is not None
