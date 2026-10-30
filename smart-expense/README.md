# Application directory

See the [repository guide](../README.md) for exact setup commands and the [Part 2 checklist](../docs/part2/readiness.md).

Use PostgreSQL for deployment. Copy `.env.example` to `.env`, configure `DB_PASSWORD`, then run `docker compose up --build`. For local SQLite demonstrations, follow the root guide. Administrative interface: `/django-admin/`.

Production requires `DJANGO_ENV=production`, a random `DJANGO_SECRET_KEY` of at least 50 characters, `DJANGO_DEBUG=false`, allowed hosts, and an HTTPS-capable reverse proxy. Set `TRUST_PROXY_SSL_HEADER=true` only when that proxy strips untrusted forwarding headers. Never expose the development server publicly.
