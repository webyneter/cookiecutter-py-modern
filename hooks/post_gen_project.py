#!/usr/bin/env python3
"""Post-generation hook to clean up conditional files and directories."""

import shutil
from pathlib import Path

PROJECT_DIR = Path.cwd()

DOCKER = "{{ cookiecutter.docker }}" == "True"
WEB = "{{ cookiecutter.web }}" == "True"
API = "{{ cookiecutter.api }}" == "True"


def remove_path(path: Path) -> None:
    """Remove a file or directory if it exists."""
    if path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def main() -> None:
    """Clean up files and directories based on cookiecutter options."""
    docker_dir = PROJECT_DIR / "docker"
    docker_compose = PROJECT_DIR / "docker-compose.yaml"
    dockerignore = PROJECT_DIR / ".dockerignore"

    if not DOCKER:
        remove_path(docker_dir)
        remove_path(docker_compose)
        remove_path(dockerignore)
    else:
        if not WEB:
            remove_path(docker_dir / "web")

        if not API:
            remove_path(docker_dir / "api")


if __name__ == "__main__":
    main()
