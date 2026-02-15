# Setup after using this template

1. **Clone** your new repository.
2. **Run once:** `python3 scripts/init_project.py "Your Project Name"`
    - Configures project name across the codebase.
    - Copies `.env.example` to `.env` (if `.env` does not exist).
    - Runs `poetry install`.
3. **Edit** `.env` and set DB_NAME, MINIO_BUCKET_NAME, etc. as needed.
4. **Run:** `python manage.py makemigrations` and `python manage.py migrate` then `python manage.py runserver`.

See the root [README.md](../README.md) for full instructions.
