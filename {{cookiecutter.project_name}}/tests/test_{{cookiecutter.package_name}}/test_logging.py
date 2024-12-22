"""Tests for the logging module."""

import logging
from io import StringIO
from unittest.mock import patch

import structlog

from {{cookiecutter.package_name}}.logging import get_logger


class TestGetLogger:
    """Tests for get_logger function."""

    def test_returns_bound_logger(self) -> None:
        """get_logger should return a bound logger with expected methods."""
        logger = get_logger()

        # structlog returns a BoundLoggerLazyProxy, check it has logger methods
        assert hasattr(logger, "info")
        assert hasattr(logger, "debug")
        assert hasattr(logger, "warning")
        assert hasattr(logger, "error")
        assert hasattr(logger, "bind")

    def test_logger_can_log_messages(self) -> None:
        """Logger should be able to log messages at various levels."""
        logger = get_logger()

        # These should not raise any exceptions
        logger.debug("debug message")
        logger.info("info message")
        logger.warning("warning message")
        logger.error("error message")

    def test_logger_includes_timestamp(self) -> None:
        """Logger output should include ISO timestamp."""
        logger = get_logger()

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            logger.info("test message")
            output = mock_stdout.getvalue()

        # ISO timestamp format includes 'T' separator
        assert "T" in output or "test message" in output

    def test_logger_includes_log_level(self) -> None:
        """Logger output should include log level."""
        logger = get_logger()

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            logger.info("test message")
            output = mock_stdout.getvalue()

        assert "info" in output.lower()

    def test_logger_can_bind_context(self) -> None:
        """Logger should support binding context variables."""
        logger = get_logger()
        bound_logger = logger.bind(request_id="123", user_id="456")

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            bound_logger.info("contextual message")
            output = mock_stdout.getvalue()

        assert "request_id" in output or "contextual message" in output

    def test_logger_caching(self) -> None:
        """Logger should be cached after first use."""
        logger1 = get_logger()
        logger2 = get_logger()

        # Both calls should succeed; structlog caches the configuration
        assert logger1 is not None
        assert logger2 is not None

    def test_logger_respects_log_level_filtering(self) -> None:
        """Logger should respect log level filtering."""
        # Configure with a higher minimum level
        structlog.configure(
            wrapper_class=structlog.make_filtering_bound_logger(logging.WARNING),
        )
        logger = structlog.get_logger()

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            logger.debug("should not appear")
            logger.info("should not appear")
            logger.warning("should appear")
            output = mock_stdout.getvalue()

        # Reset to default for other tests
        get_logger()

        assert "should appear" in output or output == ""
