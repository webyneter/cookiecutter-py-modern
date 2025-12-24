#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o noclobber
set -o pipefail

help() {
    cat <<EOF
Install dependencies for a generated project using uv.

Usage: $(basename "$0") PROJECT_DIR

Arguments:
    PROJECT_DIR    Path to the generated project directory

Examples:
    $(basename "$0") .test-output/my-project
    $(basename "$0") /tmp/test-output/test-project
EOF
    return 0
}

install_dependencies() {
    local project_dir="${1}"

    echo "Installing dependencies in ${project_dir}"

    if [[ ! -f "${project_dir}/pyproject.toml" ]]; then
        echo "Error: pyproject.toml not found in ${project_dir}" >&2
        return 1
    fi

    (
        cd "${project_dir}"
        uv sync
    )

    echo "Dependencies installed successfully"
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

    install_dependencies "${project_dir}"

    return 0
}

main "$@"
