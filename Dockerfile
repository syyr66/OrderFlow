ARG PYTHON_VERSION=3.12

# ------ Base Stage -------
FROM python:${PYTHON_VERSION}-slim-trixie AS base

COPY --from=ghcr.io/astral-sh/uv:0.12.18 /uv /uvx /bin/

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/opt/venv


# ------ Development Stage ------
FROM base AS development

COPY backend/pyproject.toml backend/uv.lock ./

# install main + dev dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project

ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 8000

# Source code is going to be mounted via volumes in docker-compose
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]