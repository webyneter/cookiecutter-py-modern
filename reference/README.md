# Reference Directory

This directory contains `requirements.txt` generated from the full template variant.
Dependabot scans this file to detect outdated dependencies and create update PRs.

## How it works

1. `generate-requirements.yml` regenerates `requirements.txt` when template deps change
2. Dependabot scans `requirements.txt` and creates per-dependency PRs
3. `test-reference.yml` tests each Dependabot PR
4. After merge, `sync-reference-lockfile.yml` syncs updates back to the template

## Do NOT edit manually

The `requirements.txt` file is auto-generated. To update dependencies:

1. Modify the template's `pyproject.toml`
2. Run `uv lock` to update `uv.lock`
3. Commit and push to main
4. `generate-requirements.yml` will regenerate `requirements.txt`
