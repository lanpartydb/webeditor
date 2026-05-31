_default:
    @just --list

deps-outdated:
    uv tree --all-groups --depth 1 --no-dev --outdated

serve-dev:
    uv run flask run --debug

prod_host := "127.0.0.1"
prod_port := "8080"

# Overriding example: `just prod_host=0.0.0.0 prod_port=9090 serve-prod`
serve-prod:
    uv run granian --host {{prod_host}} --interface wsgi app:app --no-ws --port {{prod_port}}
