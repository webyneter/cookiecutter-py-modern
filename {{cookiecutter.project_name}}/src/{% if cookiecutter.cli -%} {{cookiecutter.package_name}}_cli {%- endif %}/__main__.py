"""CLI entry point for {{cookiecutter.project_name}}."""

from typing import Annotated

import typer

from {{cookiecutter.package_name}}.logging import get_logger

app = typer.Typer(
    name="{{cookiecutter.project_name}}",
    help="{{cookiecutter.friendly_name}} CLI.",
    no_args_is_help=True,
)

logger = get_logger()


@app.callback()
def main(
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Enable verbose output."),
    ] = False,
) -> None:
    """{{cookiecutter.friendly_name}} command-line interface."""
    if verbose:
        logger.debug("Verbose mode enabled.")


@app.command()
def version() -> None:
    """Show the application version."""
    typer.echo("{{cookiecutter.project_name}} v{{cookiecutter.version}}")


@app.command()
def info() -> None:
    """Show application information."""
    typer.echo("{{cookiecutter.friendly_name}}")
    typer.echo("Author: {{cookiecutter.author}}")


if __name__ == "__main__":
    app()
