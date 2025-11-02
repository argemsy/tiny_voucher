# ================================
# 🏗️ Base Stage — Python + Poetry
# ================================
FROM python:3.12-slim AS python-base

# --- System setup ---
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/root/.local/bin:$PATH"

# --- Install dependencies needed for builds ---
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# --- Install Poetry globally ---
RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false

WORKDIR /app

# Copy dependency files first (for Docker cache optimization)
COPY pyproject.toml poetry.lock /app/

# Install base dependencies (no dev yet)
RUN poetry install --no-interaction --no-ansi --without dev --no-root



# ==========================
# 🧑‍💻 Development Stage
# ==========================
FROM python-base AS development

# Install dev dependencies
RUN poetry install --no-interaction --no-ansi

# Copy all project files
COPY . /app/

# Expose development port
EXPOSE 9000

# Default command: Django + FastAPI (ASGI)
CMD ["uvicorn", "config.asgi:fastapp", "--host", "0.0.0.0", "--port", "9000", "--reload"]


# ==========================
# 🧪 Testing Stage (optional)
# ==========================
FROM development AS testing

# Run migrations before testing
RUN python manage.py migrate --noinput
CMD ["pytest", "-v", "--disable-warnings", "--maxfail=1"]


# ==========================
# 🚀 Production Stage
# ==========================
FROM python-base AS production

# Use production settings
ENV DJANGO_SETTINGS_MODULE="config.settings.production"

# Copy the application source code
COPY . /app/

# Run collectstatic at build time (only once)
RUN python manage.py collectstatic --noinput

# Expose production port
EXPOSE 8000

# Copy and set execution permissions for startup scripts
COPY ./run.sh ./run-uvicorn.sh ./run-django.sh /
RUN chmod +x /run.sh /run-uvicorn.sh /run-django.sh

# Healthcheck for container orchestration (optional)
HEALTHCHECK CMD curl --fail http://localhost:8000/health || exit 1

# Run migrations and start FastAPI + Django ASGI app
CMD ["/run.sh"]
