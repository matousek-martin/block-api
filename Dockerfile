FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

ENV PYTHONPATH "${PYTHONPATH}:/"
ENV PORT=8000
ENV POETRY_VERSION=1.2.2

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 - && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy using poetry.lock* in case it doesn't exist yet
COPY pyproject.toml ./poetry.lock* /app/

RUN poetry install --no-root --without dev

COPY app /app

COPY ./entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh
