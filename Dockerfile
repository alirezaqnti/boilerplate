FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VERSION=2.1.3
WORKDIR /app

# Install libmagic for python-magic (file type detection)
RUN apt-get update && apt-get install -y --no-install-recommends libmagic1 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install "poetry==${POETRY_VERSION}"

COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-root --only main

COPY . /app
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

