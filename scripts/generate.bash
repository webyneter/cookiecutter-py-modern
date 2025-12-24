#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o noclobber
set -o pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_DIR="$(dirname "${SCRIPT_DIR}")"
DEFAULT_OUTPUT_DIR="${TEMPLATE_DIR}/.test-output"

OUTPUT_DIR="${DEFAULT_OUTPUT_DIR}"
PROJECT_NAME="test-project"
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

help() {
    cat <<EOF
Generate a project from the cookiecutter template.

Usage: $(basename "$0") [OPTIONS]

Options:
    -h, --help                   Show this help message
    -o, --output DIR             Output directory (default: ${DEFAULT_OUTPUT_DIR})
    -n, --name NAME              Project name (default: ${PROJECT_NAME})
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
    --clean                      Remove project directory if it exists before generation

Examples:
    $(basename "$0") --name my-project --api true --web false
    $(basename "$0") --clean --name full-project --api true --api-auth true
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

generate_project() {
    local output_dir="${1}"
    local project_name="${2}"
    local sentry_val="${3}"
    local async_val="${4}"
    local cli_val="${5}"
    local web_val="${6}"
    local api_val="${7}"
    local api_auth_val="${8}"
    local api_lambda_val="${9}"
    local api_lambda_tracing_val="${10}"
    local api_lambda_metrics_val="${11}"
    local api_pagination_val="${12}"
    local api_versioning_val="${13}"
    local docker_val="${14}"

    echo "Generating project '${project_name}' with options:"
    echo "  sentry=${sentry_val}, async=${async_val}, cli=${cli_val}, web=${web_val}"
    echo "  api=${api_val}, api_auth=${api_auth_val}, api_lambda=${api_lambda_val}"
    echo "  api_lambda_tracing=${api_lambda_tracing_val}, api_lambda_metrics=${api_lambda_metrics_val}"
    echo "  api_pagination=${api_pagination_val}, api_versioning=${api_versioning_val}"
    echo "  docker=${docker_val}"
    echo "  output: ${output_dir}/${project_name}"

    local config_file
    config_file=$(mktemp)
    cat >| "${config_file}" <<EOF
default_context:
    project_name: "${project_name}"
    author: "Test Author"
    email: "test@example.com"
    github_user: "testuser"
    license: "MIT"
    classifiers_intended_audience: "Intended Audience :: Developers"
    classifiers_development_status: "Development Status :: 3 - Alpha"
    classifiers_environment: "Environment :: Console"
    classifiers_typing: "Typing :: Typed"
    format_line_length: 120
    docker: ${docker_val}
    sentry: ${sentry_val}
    async: ${async_val}
    cli: ${cli_val}
    web: ${web_val}
    api: ${api_val}
    api_auth: ${api_auth_val}
    api_lambda: ${api_lambda_val}
    api_lambda_powertools_tracing: ${api_lambda_tracing_val}
    api_lambda_powertools_metrics: ${api_lambda_metrics_val}
    api_pagination: ${api_pagination_val}
    api_versioning: ${api_versioning_val}
    include_uv_lock: true
EOF

    cookiecutter "${TEMPLATE_DIR}" \
        --no-input \
        --config-file "${config_file}" \
        --output-dir "${output_dir}" \
        -f

    rm -f "${config_file}"

    echo "Project generated successfully at ${output_dir}/${project_name}"
}

main() {
    local clean="false"

    while [[ $# -gt 0 ]]; do
        case "${1}" in
            -h|--help)
                help
                return 0
                ;;
            -o|--output)
                OUTPUT_DIR="${2}"
                shift 2
                ;;
            -n|--name)
                PROJECT_NAME="${2}"
                shift 2
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
            --clean)
                clean="true"
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

    mkdir -p "${OUTPUT_DIR}"

    local project_dir="${OUTPUT_DIR}/${PROJECT_NAME}"

    if [[ "${clean}" == "true" ]] && [[ -d "${project_dir}" ]]; then
        echo "Removing existing project directory: ${project_dir}"
        rm -rf "${project_dir}"
    fi

    generate_project "${OUTPUT_DIR}" "${PROJECT_NAME}" "${SENTRY}" "${ASYNC}" "${CLI}" "${WEB}" "${API}" "${API_AUTH}" "${API_LAMBDA}" "${API_LAMBDA_TRACING}" "${API_LAMBDA_METRICS}" "${API_PAGINATION}" "${API_VERSIONING}" "${DOCKER}"

    return 0
}

main "$@"
