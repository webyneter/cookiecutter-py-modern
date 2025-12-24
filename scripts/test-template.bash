#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o noclobber
set -o pipefail

cleanup() {
    echo ""
    echo "Interrupted. Cleaning up..."
    kill -- -$$ 2>/dev/null || true
    exit 130
}

trap cleanup SIGINT SIGTERM

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_DIR="$(dirname "${SCRIPT_DIR}")"
DEFAULT_OUTPUT_DIR="${TEMPLATE_DIR}/.test-output"

SENTRY="true"
ASYNC="true"
CLI="true"
WEB="true"
API="true"
API_AUTH="true"
API_LAMBDA="true"
API_LAMBDA_TRACING="true"
API_LAMBDA_METRICS="true"
API_PAGINATION="true"
API_VERSIONING="true"
DOCKER="true"
OUTPUT_DIR="${DEFAULT_OUTPUT_DIR}"
PROJECT_NAME="test-project"
INSTALL_DEPS="true"
RUN_TESTS="true"
RUN_LINT="true"
RUN_ALL_VARIANTS="true"
CLEAN="true"

help() {
    cat <<EOF
Generate a project from the cookiecutter template for testing purposes.

This is an orchestration script that calls individual scripts:
  - generate.bash: Generate project from template
  - install.bash: Install dependencies
  - lint.bash: Run linting and type checks
  - test.bash: Run tests
  - test-all-variants.bash: Test all variant combinations

Usage: $(basename "$0") [OPTIONS]

Options:
    -h, --help                   Show this help message
    -s, --sentry BOOL            Enable Sentry integration (default: ${SENTRY})
    -a, --async BOOL             Enable async support (default: ${ASYNC})
    -c, --cli BOOL               Enable CLI support (default: ${CLI})
    -w, --web BOOL               Enable web/Django support (default: ${WEB})
    --api BOOL                   Enable FastAPI support (default: ${API})
    --api-auth BOOL              Enable API auth support (default: ${API_AUTH})
    --api-lambda BOOL            Enable AWS Lambda hosting (default: ${API_LAMBDA})
    --api-lambda-tracing BOOL    Enable Powertools tracing (default: ${API_LAMBDA_TRACING})
    --api-lambda-metrics BOOL    Enable Powertools metrics (default: ${API_LAMBDA_METRICS})
    --api-pagination BOOL        Enable pagination utilities (default: ${API_PAGINATION})
    --api-versioning BOOL        Enable API versioning (default: ${API_VERSIONING})
    -d, --docker BOOL            Enable Docker support (default: ${DOCKER})
    -o, --output DIR             Output directory (default: ${DEFAULT_OUTPUT_DIR})
    -n, --name NAME              Project name (default: ${PROJECT_NAME})
    -i, --install                Install dependencies after generation
    -t, --test                   Run tests after generation (implies --install)
    -l, --lint                   Run linting/type checks after generation (implies --install)
    --all-variants BOOL          Generate and test all variant combinations (default: ${RUN_ALL_VARIANTS})
    --clean                      Remove output directory before generation

Examples:
    $(basename "$0")
        Test all variant combinations (default)

    $(basename "$0") --clean
        Clean output and test all variant combinations

    $(basename "$0") --all-variants false --web true --async true
        Generate and test a single project with specific options

    $(basename "$0") --all-variants false --clean --web true --test
        Clean, generate web project, install deps, and run tests
EOF
    return 0
}

parse_bool() {
    local value="${1}"
    case "${value}" in
        true|True|TRUE|1|yes|Yes|YES)
            echo "true"
            ;;
        false|False|FALSE|0|no|No|NO)
            echo "false"
            ;;
        *)
            echo "Invalid boolean value: ${value}" >&2
            return 1
            ;;
    esac
}

main() {
    while [[ $# -gt 0 ]]; do
        case "${1}" in
            -h|--help)
                help
                return 0
                ;;
            -s|--sentry)
                SENTRY=$(parse_bool "${2}")
                shift 2
                ;;
            -a|--async)
                ASYNC=$(parse_bool "${2}")
                shift 2
                ;;
            -c|--cli)
                CLI=$(parse_bool "${2}")
                shift 2
                ;;
            -w|--web)
                WEB=$(parse_bool "${2}")
                shift 2
                ;;
            --api)
                API=$(parse_bool "${2}")
                shift 2
                ;;
            --api-auth)
                API_AUTH=$(parse_bool "${2}")
                shift 2
                ;;
            --api-lambda)
                API_LAMBDA=$(parse_bool "${2}")
                shift 2
                ;;
            --api-lambda-tracing)
                API_LAMBDA_TRACING=$(parse_bool "${2}")
                shift 2
                ;;
            --api-lambda-metrics)
                API_LAMBDA_METRICS=$(parse_bool "${2}")
                shift 2
                ;;
            --api-pagination)
                API_PAGINATION=$(parse_bool "${2}")
                shift 2
                ;;
            --api-versioning)
                API_VERSIONING=$(parse_bool "${2}")
                shift 2
                ;;
            -d|--docker)
                DOCKER=$(parse_bool "${2}")
                shift 2
                ;;
            -o|--output)
                OUTPUT_DIR="${2}"
                shift 2
                ;;
            -n|--name)
                PROJECT_NAME="${2}"
                shift 2
                ;;
            -i|--install)
                INSTALL_DEPS="true"
                shift
                ;;
            -t|--test)
                RUN_TESTS="true"
                INSTALL_DEPS="true"
                shift
                ;;
            -l|--lint)
                RUN_LINT="true"
                INSTALL_DEPS="true"
                shift
                ;;
            --all-variants)
                RUN_ALL_VARIANTS=$(parse_bool "${2}")
                shift 2
                ;;
            --clean)
                CLEAN="true"
                shift
                ;;
            *)
                echo "Unknown option: ${1}" >&2
                help >&2
                return 1
                ;;
        esac
    done

    if ! command -v cookiecutter &> /dev/null; then
        echo "Error: cookiecutter is not installed. Install with: pipx install cookiecutter" >&2
        return 1
    fi

    if ! command -v uv &> /dev/null; then
        echo "Error: uv is not installed. See: https://docs.astral.sh/uv/getting-started/installation/" >&2
        return 1
    fi

    if [[ "${CLEAN}" == "true" ]] && [[ -d "${OUTPUT_DIR}" ]]; then
        echo "Cleaning output directory: ${OUTPUT_DIR}"
        rm -rf "${OUTPUT_DIR}"
    fi

    mkdir -p "${OUTPUT_DIR}"

    if [[ "${RUN_ALL_VARIANTS}" == "true" ]]; then
        "${SCRIPT_DIR}/test-all-variants.bash" --output "${OUTPUT_DIR}"
        return $?
    fi

    local project_dir="${OUTPUT_DIR}/${PROJECT_NAME}"

    "${SCRIPT_DIR}/generate.bash" \
        --output "${OUTPUT_DIR}" \
        --name "${PROJECT_NAME}" \
        --sentry "${SENTRY}" \
        --async "${ASYNC}" \
        --cli "${CLI}" \
        --web "${WEB}" \
        --api "${API}" \
        --api-auth "${API_AUTH}" \
        --api-lambda "${API_LAMBDA}" \
        --api-lambda-tracing "${API_LAMBDA_TRACING}" \
        --api-lambda-metrics "${API_LAMBDA_METRICS}" \
        --api-pagination "${API_PAGINATION}" \
        --api-versioning "${API_VERSIONING}" \
        --docker "${DOCKER}" \
        --clean

    if [[ "${INSTALL_DEPS}" == "true" ]]; then
        "${SCRIPT_DIR}/install.bash" "${project_dir}"
    fi

    if [[ "${RUN_LINT}" == "true" ]]; then
        "${SCRIPT_DIR}/lint.bash" "${project_dir}"
    fi

    if [[ "${RUN_TESTS}" == "true" ]]; then
        "${SCRIPT_DIR}/test.bash" "${project_dir}"
    fi

    return 0
}

main "$@"
