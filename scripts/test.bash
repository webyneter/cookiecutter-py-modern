#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o noclobber
set -o pipefail

help() {
    cat <<EOF
Run tests for a generated project using pytest.

Usage: $(basename "$0") PROJECT_DIR [COMMAND]

Arguments:
    PROJECT_DIR    Path to the generated project directory

Commands:
    unit           Run unit tests with coverage (default)
    integration    Run integration tests against Docker Compose Lambda
                   (automatically starts/stops Docker Compose)

Examples:
    $(basename "$0") .test-output/my-project
    $(basename "$0") .test-output/my-project unit
    $(basename "$0") .test-output/my-project integration
EOF
    return 0
}

wait_for_lambda_rie() {
    local max_attempts=30
    local attempt=1

    echo "Waiting for Lambda RIE to be ready..."
    while [[ ${attempt} -le ${max_attempts} ]]; do
        if curl -s http://localhost:9000/2015-03-31/functions/function/invocations \
            -d '{"httpMethod":"GET","path":"/health","headers":{},"body":""}' 2>/dev/null | grep -q "statusCode"; then
            echo "Lambda RIE is ready"
            return 0
        fi
        echo "Waiting... (${attempt}/${max_attempts})"
        sleep 2
        ((attempt++))
    done

    echo "Error: Lambda RIE did not become ready in time" >&2
    return 1
}

run_unit_tests() {
    local project_dir="${1}"

    echo "Running unit tests in ${project_dir}"

    (
        cd "${project_dir}"
        uv run pytest tests/unit/
    )

    echo "Unit tests completed"
}

run_integration_tests() {
    local project_dir="${1}"

    echo "Running integration tests in ${project_dir}"

    # Check if integration tests directory exists
    if [[ ! -d "${project_dir}/tests/integration" ]]; then
        echo "No integration tests found (tests/integration/ does not exist)"
        echo "Integration tests are only available when api_lambda=true"
        return 0
    fi

    (
        cd "${project_dir}"

        # Check if docker-compose.yaml exists
        if [[ ! -f "docker-compose.yaml" ]]; then
            echo "Error: docker-compose.yaml not found" >&2
            return 1
        fi

        echo "Starting Docker Compose services..."
        docker compose up -d --build

        # Wait for Lambda RIE to be ready
        if ! wait_for_lambda_rie; then
            echo "Docker Compose logs:"
            docker compose logs
            docker compose down -v
            return 1
        fi

        echo "Running integration tests..."
        local test_exit_code=0
        uv run pytest tests/integration/ --no-cov -v || test_exit_code=$?

        echo "Stopping Docker Compose services..."
        docker compose down -v

        return ${test_exit_code}
    )

    echo "Integration tests completed"
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
    local command="${2:-unit}"

    if [[ ! -d "${project_dir}" ]]; then
        echo "Error: Directory does not exist: ${project_dir}" >&2
        return 1
    fi

    if ! command -v uv &> /dev/null; then
        echo "Error: uv is not installed. See: https://docs.astral.sh/uv/getting-started/installation/" >&2
        return 1
    fi

    case "${command}" in
        unit)
            run_unit_tests "${project_dir}"
            ;;
        integration)
            if ! command -v docker &> /dev/null; then
                echo "Error: docker is not installed" >&2
                return 1
            fi
            run_integration_tests "${project_dir}"
            ;;
        *)
            echo "Error: Unknown command: ${command}" >&2
            help >&2
            return 1
            ;;
    esac

    return 0
}

main "$@"
