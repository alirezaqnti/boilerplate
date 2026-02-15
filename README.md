# Django REST API Backend (Template)

A **GitHub template** for a Django 6 REST API with DRF, JWT auth, Redis cache, PostgreSQL, and optional MinIO/S3 storage. Use this repository as a template to create new projects with one-click setup and a single initiation step to configure your project name everywhere.

---

## Use this template

1. **Create a new repository from this template**

    - Click **Use this template** → **Create a new repository** on GitHub.
    - Clone your new repo locally.

2. **Run project initiation (required once)**
   Configure the project name, slug, and package name across the codebase:

    ```bash
    python3 scripts/init_project.py "Your Project Name"
    ```

    (Use `python` if your system aliases it to Python 3.)

    Or interactively:

    ```bash
    python3 scripts/init_project.py
    ```

    Enter the display name when prompted.

    Options:

    - `--slug` – Slug for containers, DB, cache (default: derived from name, e.g. `your-project-name`).
    - `--package` – Python package name in `pyproject.toml` (default: `<slug>-backend`).
    - `--dry-run` – Show what would be set without changing files.

    This updates:

    - `pyproject.toml` (package name)
    - `docker-compose.yml` (container names, default DB/bucket)
    - `core/settings.py` (cache key prefix)
    - `core/packages/drf_spectacular.py` (API docs title)
    - `common/admins/base.py` (admin site title)
    - Writes `project_config.json` with your choices.

3. **Configure environment and run**
    ```bash
    cp .env.example .env
    # Edit .env: DB_NAME, MINIO_BUCKET_NAME, etc. (defaults match your slug after init)
    # Optional: set SENTRY_DSN to enable Sentry error monitoring and performance tracing
    poetry install
    python manage.py migrate
    python manage.py runserver
    ```

---

## Tech stack

-   Python 3.12+, Django 6, Django REST Framework 3.16
-   drf-spectacular (OpenAPI), drf-simplejwt, django-redis, django-filter
-   PostgreSQL, Redis (cache), MinIO/S3 (media/static), Sentry (optional)
-   Poetry for dependency management

## Project rules and structure

See [.cursorrules](.cursorrules) for Cursor AI and coding conventions (base models, views, OpenAPI, admin, services layer).

## Making this repo a template on GitHub

In your GitHub repository: **Settings** → **General** → check **Template repository**. After that, others can use **Use this template** to create a new repo from it.
