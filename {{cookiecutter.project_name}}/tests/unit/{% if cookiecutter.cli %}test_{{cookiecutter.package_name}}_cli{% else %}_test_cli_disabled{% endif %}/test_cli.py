"""Tests for the CLI module."""

from typer.testing import CliRunner

from {{cookiecutter.package_name}}_cli import app

runner = CliRunner()


class TestApp:
    """Tests for the main CLI app."""

    def test_app_exists(self) -> None:
        """CLI app should be importable."""
        assert app is not None

    def test_no_args_shows_help(self) -> None:
        """Running without arguments should show help."""
        result = runner.invoke(app)

        # Typer with no_args_is_help=True may return exit code 0 or 2
        assert result.exit_code in (0, 2)
        assert "Usage:" in result.stdout or "--help" in result.stdout

    def test_help_option(self) -> None:
        """--help should show usage information."""
        result = runner.invoke(app, ["--help"])

        assert result.exit_code == 0
        assert "Usage:" in result.stdout or "{{cookiecutter.project_name}}" in result.stdout


class TestVersionCommand:
    """Tests for the version command."""

    def test_shows_version(self) -> None:
        """version command should display version string."""
        result = runner.invoke(app, ["version"])

        assert result.exit_code == 0
        assert "{{cookiecutter.project_name}}" in result.stdout
        assert "{{cookiecutter.version}}" in result.stdout


class TestInfoCommand:
    """Tests for the info command."""

    def test_shows_info(self) -> None:
        """info command should display application information."""
        result = runner.invoke(app, ["info"])

        assert result.exit_code == 0
        assert "{{cookiecutter.friendly_name}}" in result.stdout
        assert "{{cookiecutter.author}}" in result.stdout


class TestVerboseOption:
    """Tests for the verbose option."""

    def test_verbose_flag_accepted(self) -> None:
        """--verbose flag should be accepted."""
        result = runner.invoke(app, ["--verbose", "version"])

        assert result.exit_code == 0

    def test_verbose_short_flag_accepted(self) -> None:
        """-v flag should be accepted."""
        result = runner.invoke(app, ["-v", "version"])

        assert result.exit_code == 0
