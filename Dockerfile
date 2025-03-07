FROM python:3.13.2-slim

ENV POETRY_HOME=/opt/poetry

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry

# Copy project files
COPY pyproject.toml poetry.lock* ./
COPY src/ ./src/

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Create logs directory
RUN mkdir -p logs

# Set the entrypoint
CMD ["poetry", "run", "python", "-m", "web_url_scanner.scanner"] 