#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o noclobber
set -o pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_DIR="$(dirname "${SCRIPT_DIR}")"
DEFAULT_OUTPUT_DIR="${TEMPLATE_DIR}/.test-output"

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
PYCHARM="true"
OUTPUT_DIR="${DEFAULT_OUTPUT_DIR}"
PROJECT_NAME="test-project"
INSTALL_DEPS="false"
RUN_TESTS="true"
RUN_LINT="true"
CLEAN="false"

help() {
    cat <<EOF
Generate a project from the cookiecutter template for testing purposes.

Usage: $(basename "$0") [OPTIONS]

Options:
    -h, --help                   Show this help message
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
    -p, --pycharm BOOL           Enable PyCharm support (default: ${PYCHARM})
    -o, --output DIR             Output directory (default: ${DEFAULT_OUTPUT_DIR})
    -n, --name NAME              Project name (default: ${PROJECT_NAME})
    -i, --install                Install dependencies after generation
    -t, --test                   Run tests after generation (implies --install)
    -l, --lint                   Run linting/type checks after generation (implies --install)
    --clean                      Remove output directory before generation
    --all-variants               Generate and test all variant combinations

Examples:
    $(basename "$0")
        Generate with defaults (async + cli)

    $(basename "$0") --web true --async true --install
        Generate async web project and install deps

    $(basename "$0") --all-variants
        Test all variant combinations

    $(basename "$0") --clean --web true --test
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

generate_project() {
    local output_dir="${1}"
    local project_name="${2}"
    local async_val="${3}"
    local cli_val="${4}"
    local web_val="${5}"
    local api_val="${6}"
    local api_auth_val="${7}"
    local api_lambda_val="${8}"
    local api_lambda_tracing_val="${9}"
    local api_lambda_metrics_val="${10}"
    local api_pagination_val="${11}"
    local api_versioning_val="${12}"
    local docker_val="${13}"
    local pycharm_val="${14}"

    echo "Generating project '${project_name}' with options:"
    echo "  async=${async_val}, cli=${cli_val}, web=${web_val}"
    echo "  api=${api_val}, api_auth=${api_auth_val}, api_lambda=${api_lambda_val}"
    echo "  api_lambda_tracing=${api_lambda_tracing_val}, api_lambda_metrics=${api_lambda_metrics_val}"
    echo "  api_pagination=${api_pagination_val}, api_versioning=${api_versioning_val}"
    echo "  docker=${docker_val}, pycharm=${pycharm_val}"
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
    pycharm: ${pycharm_val}
    docker: ${docker_val}
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

run_tests() {
    local project_dir="${1}"

    echo "Running tests in ${project_dir}"

    (
        cd "${project_dir}"
        uv run pytest
    )

    echo "Tests completed"
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

test_all_variants() {
    local output_dir="${1}"
    # Format: async:cli:web:api:api_auth:api_lambda:api_lambda_tracing:api_lambda_metrics:api_pagination:api_versioning:name
    local variants=(
        "false:false:false:false:false:false:false:false:false:false:minimal"
        "true:false:false:false:false:false:false:false:false:false:async-only"
        "false:true:false:false:false:false:false:false:false:false:cli-only"
        "false:false:true:false:false:false:false:false:false:false:web-only"
        "false:false:false:true:false:false:false:false:false:false:api-only"
        "false:false:false:true:true:false:false:false:false:false:api-auth"
        "false:false:false:true:false:true:false:false:false:false:api-lambda"
        "false:false:false:true:false:true:true:false:false:false:api-lambda-traced"
        "false:false:false:true:false:true:true:true:false:false:api-lambda-full"
        "false:false:false:true:false:false:false:false:true:false:api-pagination"
        "false:false:false:true:false:false:false:false:false:true:api-versioning"
        "true:true:false:false:false:false:false:false:false:false:async-cli"
        "true:false:true:false:false:false:false:false:false:false:async-web"
        "true:false:false:true:false:false:false:false:false:false:async-api"
        "true:false:false:true:true:false:false:false:false:false:async-api-auth"
        "true:false:false:true:true:true:true:true:true:true:async-api-full"
        "true:true:true:false:false:false:false:false:false:false:full-no-api"
        "true:true:false:true:true:false:false:false:false:false:full-no-web"
        "true:true:true:true:true:true:true:true:true:true:full"
    )

    local failed=()
    local passed=()

    for variant in "${variants[@]}"; do
        IFS=':' read -r async_val cli_val web_val api_val api_auth_val api_lambda_val api_lambda_tracing_val api_lambda_metrics_val api_pagination_val api_versioning_val name <<< "${variant}"
        local project_name="test-${name}"
        local project_dir="${output_dir}/${project_name}"

        echo ""
        echo "========================================"
        echo "Testing variant: ${name}"
        echo "========================================"

        if [[ -d "${project_dir}" ]]; then
            rm -rf "${project_dir}"
        fi

        if generate_project "${output_dir}" "${project_name}" "${async_val}" "${cli_val}" "${web_val}" "${api_val}" "${api_auth_val}" "${api_lambda_val}" "${api_lambda_tracing_val}" "${api_lambda_metrics_val}" "${api_pagination_val}" "${api_versioning_val}" "true" "false"; then
            if install_dependencies "${project_dir}"; then
                if run_lint "${project_dir}"; then
                    if run_tests "${project_dir}"; then
                        passed+=("${name}")
                        echo "PASSED: ${name}"
                    else
                        failed+=("${name} (tests failed)")
                        echo "FAILED: ${name} (tests failed)"
                    fi
                else
                    failed+=("${name} (lint failed)")
                    echo "FAILED: ${name} (lint failed)"
                fi
            else
                failed+=("${name} (install failed)")
                echo "FAILED: ${name} (install failed)"
            fi
        else
            failed+=("${name} (generation failed)")
            echo "FAILED: ${name} (generation failed)"
        fi
    done

    echo ""
    echo "========================================"
    echo "Summary"
    echo "========================================"
    echo "Passed: ${#passed[@]}"
    for p in "${passed[@]}"; do
        echo "  - ${p}"
    done
    echo "Failed: ${#failed[@]}"
    for f in "${failed[@]}"; do
        echo "  - ${f}"
    done

    if [[ ${#failed[@]} -gt 0 ]]; then
        return 1
    fi
    return 0
}

main() {
    local all_variants="false"

    while [[ $# -gt 0 ]]; do
        case "${1}" in
            -h|--help)
                help
                return 0
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
            -p|--pycharm)
                PYCHARM=$(parse_bool "${2}")
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
            --clean)
                CLEAN="true"
                shift
                ;;
            --all-variants)
                all_variants="true"
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

    if [[ "${all_variants}" == "true" ]]; then
        test_all_variants "${OUTPUT_DIR}"
        return $?
    fi

    local project_dir="${OUTPUT_DIR}/${PROJECT_NAME}"

    if [[ -d "${project_dir}" ]]; then
        echo "Removing existing project directory: ${project_dir}"
        rm -rf "${project_dir}"
    fi

    generate_project "${OUTPUT_DIR}" "${PROJECT_NAME}" "${ASYNC}" "${CLI}" "${WEB}" "${API}" "${API_AUTH}" "${API_LAMBDA}" "${API_LAMBDA_TRACING}" "${API_LAMBDA_METRICS}" "${API_PAGINATION}" "${API_VERSIONING}" "${DOCKER}" "${PYCHARM}"

    if [[ "${INSTALL_DEPS}" == "true" ]]; then
        install_dependencies "${project_dir}"
    fi

    if [[ "${RUN_TESTS}" == "true" ]]; then
        run_tests "${project_dir}"
    fi

    if [[ "${RUN_LINT}" == "true" ]]; then
        run_lint "${project_dir}"
    fi

    return 0
}

main "$@"
