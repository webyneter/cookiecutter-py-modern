#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o noclobber
set -o pipefail

help() {
    cat <<EOF
Run linting and type checks for a generated project.

Runs the following checks:
  - ruff check (linting)
  - ruff format --check (formatting)
  - mypy (type checking)
  - vulture (dead code detection)

Usage: $(basename "$0") PROJECT_DIR

Arguments:
    PROJECT_DIR    Path to the generated project directory

Examples:
    $(basename "$0") .test-output/my-project
    $(basename "$0") /tmp/test-output/test-project
EOF
    return 0
}

run_lint() {
    local project_dir="${1}"

    echo "Running linting and type checks in ${project_dir}"

    (
        cd "${project_dir}"

        echo "Running ruff check..."
        uv run ruff check --no-fix .

        echo "Running ruff format check..."
        uv run ruff format --check .

        echo "Running mypy..."
        uv run mypy src/

        echo "Running vulture..."
        uv run vulture src/ --min-confidence 80
    )

    echo "Linting and type checks completed"
}

main() {
    if [[ $# -lt 1 ]]; then
        echo "Error: PROJECT_DIR argument is required" >&2
        help >&2
        return 1
    fi

    case "${1}" in
        -h|--help)
            help
            return 0
            ;;
    esac

    local project_dir="${1}"

    if [[ ! -d "${project_dir}" ]]; then
        echo "Error: Directory does not exist: ${project_dir}" >&2
        return 1
    fi

    if ! command -v uv &> /dev/null; then
        echo "Error: uv is not installed. See: https://docs.astral.sh/uv/getting-started/installation/" >&2
        return 1
    fi

    run_lint "${project_dir}"

    return 0
}

main "$@"
