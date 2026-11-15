# Configuration and Setup Guide

## Purpose
This document describes configuration practices for the Smart Expense & Budget Management application.

## Environment Configuration

Keep environment-specific configuration outside source code.

Typical configuration values may include:

- Django secret key.
- Debug mode.
- Database connection settings.
- Allowed hosts.
- Other environment-specific service settings.

## Security Practices

- Do not commit `.env` files containing secrets.
- Do not publish passwords, tokens, or private keys.
- Use separate configuration for development and production.
- Keep debug mode disabled in production.
- Restrict access to application credentials.

## Database Setup

1. Configure the database connection.
2. Apply the project's migrations.
3. Verify that the application can access the database.

Run migrations with:

    python manage.py migrate

## Static Files

Collect static files when preparing a deployment:

    python manage.py collectstatic

## Final Verification

Run the Django system check and relevant automated tests after changing configuration.
