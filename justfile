_default:
    @just --list

deps-outdated:
    uv tree --all-groups --depth 1 --no-dev --outdated

serve-dev:
    uv run flask run --debug

serve-prod:
    uv run granian --interface wsgi app:app --no-ws
