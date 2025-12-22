#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o noclobber
set -o pipefail

main() {
    if [[ -n "${POSTGRES_HOST:-}" ]] && [[ -n "${POSTGRES_PORT:-}" ]] && \
       [[ -n "${POSTGRES_USER:-}" ]] && [[ -n "${POSTGRES_PASSWORD:-}" ]] && \
       [[ -n "${POSTGRES_DB:-}" ]]; then
        export DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"
        echo "DATABASE_URL constructed from individual environment variables"
    fi

    exec docker-entrypoint.sh "$@"
}

main "$@"
