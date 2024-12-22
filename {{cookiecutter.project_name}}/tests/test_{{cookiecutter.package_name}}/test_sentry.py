"""Tests for the Sentry integration module."""

import importlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest_mock import MockerFixture


class TestInitSentry:
    """Tests for init_sentry function."""

    def test_skips_initialization_when_sentry_dsn_empty(
        self,
        mocker: "MockerFixture",
    ) -> None:
        """init_sentry should skip initialization when SENTRY_DSN is empty."""
        mocker.patch.dict(
            "os.environ",
            {"ENVIRONMENT": "test", "SENTRY_DSN": ""},
            clear=False,
        )

        # Re-import to pick up new env vars
        import {{cookiecutter.package_name}}.sentry as sentry_module

        sentry_module = importlib.reload(sentry_module)

        mock_sentry_init = mocker.patch("sentry_sdk.init")
        mock_logger = mocker.patch.object(sentry_module, "logger")

        sentry_module.init_sentry()

        mock_sentry_init.assert_not_called()
        mock_logger.warning.assert_called()

    def test_skips_initialization_when_environment_empty(
        self,
        mocker: "MockerFixture",
    ) -> None:
        """init_sentry should skip initialization when ENVIRONMENT is empty."""
        mocker.patch.dict(
            "os.environ",
            {"ENVIRONMENT": "", "SENTRY_DSN": "https://key@sentry.io/123"},
            clear=False,
        )

        import {{cookiecutter.package_name}}.sentry as sentry_module

        sentry_module = importlib.reload(sentry_module)

        mock_sentry_init = mocker.patch("sentry_sdk.init")
        mock_logger = mocker.patch.object(sentry_module, "logger")

        sentry_module.init_sentry()

        mock_sentry_init.assert_not_called()
        mock_logger.warning.assert_called()

    def test_initializes_sentry_with_valid_config(
        self,
        mocker: "MockerFixture",
    ) -> None:
        """init_sentry should initialize Sentry SDK with valid configuration."""
        test_dsn = "https://key@sentry.io/123"
        test_env = "production"

        mocker.patch.dict(
            "os.environ",
            {"ENVIRONMENT": test_env, "SENTRY_DSN": test_dsn},
            clear=False,
        )

        import {{cookiecutter.package_name}}.sentry as sentry_module

        sentry_module = importlib.reload(sentry_module)

        mock_sentry_init = mocker.patch("sentry_sdk.init")
        mocker.patch.object(sentry_module, "logger")

        sentry_module.init_sentry()

        mock_sentry_init.assert_called_once()
        call_kwargs = mock_sentry_init.call_args.kwargs
        assert call_kwargs["dsn"] == test_dsn
        assert call_kwargs["environment"] == test_env

    def test_includes_asyncio_integration(
        self,
        mocker: "MockerFixture",
    ) -> None:
        """init_sentry should include AsyncioIntegration."""
        mocker.patch.dict(
            "os.environ",
            {
                "ENVIRONMENT": "test",
                "SENTRY_DSN": "https://key@sentry.io/123",
            },
            clear=False,
        )

        import {{cookiecutter.package_name}}.sentry as sentry_module

        sentry_module = importlib.reload(sentry_module)

        mock_sentry_init = mocker.patch("sentry_sdk.init")
        mocker.patch.object(sentry_module, "logger")

        sentry_module.init_sentry()

        call_kwargs = mock_sentry_init.call_args.kwargs
        integrations = call_kwargs["integrations"]
        integration_types = [type(i).__name__ for i in integrations]
        assert "AsyncioIntegration" in integration_types

    def test_logs_debug_messages_during_initialization(
        self,
        mocker: "MockerFixture",
    ) -> None:
        """init_sentry should log debug messages during initialization."""
        mocker.patch.dict(
            "os.environ",
            {
                "ENVIRONMENT": "staging",
                "SENTRY_DSN": "https://key@sentry.io/123",
            },
            clear=False,
        )

        import {{cookiecutter.package_name}}.sentry as sentry_module

        sentry_module = importlib.reload(sentry_module)

        mocker.patch("sentry_sdk.init")
        mock_logger = mocker.patch.object(sentry_module, "logger")

        sentry_module.init_sentry()

        assert mock_logger.debug.call_count == 2


class TestModuleLevelConfiguration:
    """Tests for module-level configuration."""

    def test_env_instance_created(self, mocker: "MockerFixture") -> None:
        """Module should create an Env instance."""
        mocker.patch.dict(
            "os.environ",
            {"ENVIRONMENT": "test", "SENTRY_DSN": ""},
            clear=False,
        )

        import {{cookiecutter.package_name}}.sentry as sentry_module

        sentry_module = importlib.reload(sentry_module)

        assert sentry_module.env is not None

    def test_logger_instance_created(self, mocker: "MockerFixture") -> None:
        """Module should create a logger instance."""
        mocker.patch.dict(
            "os.environ",
            {"ENVIRONMENT": "test", "SENTRY_DSN": ""},
            clear=False,
        )

        import {{cookiecutter.package_name}}.sentry as sentry_module

        sentry_module = importlib.reload(sentry_module)

        assert sentry_module.logger is not None
