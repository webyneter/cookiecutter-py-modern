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

OUTPUT_DIR="${DEFAULT_OUTPUT_DIR}"

help() {
    cat <<EOF
Test all variant combinations of the cookiecutter template.

Generates projects with different option combinations and runs:
  1. Project generation
  2. Dependency installation
  3. Linting and type checks
  4. Tests

Usage: $(basename "$0") [OPTIONS]

Options:
    -h, --help       Show this help message
    -o, --output     Output directory (default: ${DEFAULT_OUTPUT_DIR})
    --clean          Remove output directory before starting

Variants tested:
  - minimal, cli-only, web-only, api-only, api-auth, api-lambda
  - async-web, async-api-auth, full-no-api, full-no-web, full

Examples:
    $(basename "$0")
    $(basename "$0") --clean
    $(basename "$0") --output /tmp/variants
EOF
    return 0
}

test_all_variants() {
    local output_dir="${1}"
    local variants_file="${TEMPLATE_DIR}/variants.json"

    if [[ ! -f "${variants_file}" ]]; then
        echo "Error: variants.json not found at ${variants_file}" >&2
        return 1
    fi

    local failed=()
    local passed=()
    local variant_count
    variant_count=$(jq '.variants | length' "${variants_file}")

    for ((i = 0; i < variant_count; i++)); do
        local name sentry_val async_val cli_val web_val api_val
        local api_auth_val api_lambda_val api_lambda_tracing_val api_lambda_metrics_val
        local api_pagination_val api_versioning_val

        name=$(jq -r ".variants[$i].name" "${variants_file}")
        sentry_val=$(jq -r ".variants[$i].sentry" "${variants_file}")
        async_val=$(jq -r ".variants[$i].async" "${variants_file}")
        cli_val=$(jq -r ".variants[$i].cli" "${variants_file}")
        web_val=$(jq -r ".variants[$i].web" "${variants_file}")
        api_val=$(jq -r ".variants[$i].api" "${variants_file}")
        api_auth_val=$(jq -r ".variants[$i].api_auth" "${variants_file}")
        api_lambda_val=$(jq -r ".variants[$i].api_lambda" "${variants_file}")
        api_lambda_tracing_val=$(jq -r ".variants[$i].api_lambda_tracing" "${variants_file}")
        api_lambda_metrics_val=$(jq -r ".variants[$i].api_lambda_metrics" "${variants_file}")
        api_pagination_val=$(jq -r ".variants[$i].api_pagination" "${variants_file}")
        api_versioning_val=$(jq -r ".variants[$i].api_versioning" "${variants_file}")

        local project_name="test-${name}"
        local project_dir="${output_dir}/${project_name}"

        echo ""
        echo "========================================"
        echo "Testing variant: ${name}"
        echo "========================================"

        if [[ -d "${project_dir}" ]]; then
            rm -rf "${project_dir}"
        fi

        if "${SCRIPT_DIR}/generate.bash" \
            --output "${output_dir}" \
            --name "${project_name}" \
            --sentry "${sentry_val}" \
            --async "${async_val}" \
            --cli "${cli_val}" \
            --web "${web_val}" \
            --api "${api_val}" \
            --api-auth "${api_auth_val}" \
            --api-lambda "${api_lambda_val}" \
            --api-lambda-tracing "${api_lambda_tracing_val}" \
            --api-lambda-metrics "${api_lambda_metrics_val}" \
            --api-pagination "${api_pagination_val}" \
            --api-versioning "${api_versioning_val}" \
            --docker "true"; then
            if "${SCRIPT_DIR}/install.bash" "${project_dir}"; then
                if "${SCRIPT_DIR}/lint.bash" "${project_dir}"; then
                    if "${SCRIPT_DIR}/test.bash" "${project_dir}"; then
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

    if ! command -v jq &> /dev/null; then
        echo "Error: jq is not installed. Install with your package manager (e.g., apt install jq)" >&2
        return 1
    fi

    if ! command -v cookiecutter &> /dev/null; then
        echo "Error: cookiecutter is not installed. Install with: pipx install cookiecutter" >&2
        return 1
    fi

    if ! command -v uv &> /dev/null; then
        echo "Error: uv is not installed. See: https://docs.astral.sh/uv/getting-started/installation/" >&2
        return 1
    fi

    if [[ "${clean}" == "true" ]] && [[ -d "${OUTPUT_DIR}" ]]; then
        echo "Cleaning output directory: ${OUTPUT_DIR}"
        rm -rf "${OUTPUT_DIR}"
    fi

    mkdir -p "${OUTPUT_DIR}"

    test_all_variants "${OUTPUT_DIR}"

    return $?
}

main "$@"
