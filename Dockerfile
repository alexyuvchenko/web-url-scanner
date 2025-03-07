FROM python:3.13.1-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_CREATE=false
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry

# Copy only dependency files first
COPY pyproject.toml poetry.lock* ./

# Install dependencies
RUN poetry install --no-interaction --no-ansi --no-root

# Copy source code
COPY . .

# Install the project
RUN poetry install --no-interaction --no-ansi

# Create logs directory with proper permissions
RUN mkdir -p logs && chmod 777 logs

# Set the entrypoint
CMD ["poetry", "run", "python", "-m", "web_url_scanner.scanner"] 
