# Security

The project should be developed and operated with care for account credentials and financial information.

## Reporting a vulnerability

Do not publish exploit details, credentials, tokens, or private user data in a public issue or pull request.

If you discover a security weakness, report it privately to the repository maintainers through an appropriate private communication channel. Include:

- A concise description of the affected component.
- The potential impact.
- Reproduction steps that do not expose real user data.
- Any suggested mitigation, if known.

Allow maintainers time to investigate and coordinate a fix before publicly discussing the issue.

## Handling sensitive information

- Never commit passwords, API keys, access tokens, signing keys, or production credentials.
- Keep local environment files out of version control.
- Use environment variables or an approved secret-management mechanism for configuration secrets.
- Use synthetic data for tests and demonstrations; do not commit real financial records or personal information.
- Restrict access to databases, backups, and deployment credentials to people who need it.
- If a secret is accidentally committed, treat it as exposed: revoke or rotate it and notify the maintainers. Removing it from a later commit does not make the exposed secret safe.
