FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system packages and uv
# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    libpq-dev \
    netcat-openbsd \
    postgresql-client \
    && curl -LsSf https://astral.sh/uv/install.sh | bash \
    && mv ~/.local/bin/uv /usr/local/bin/uv \
    && rm -rf ~/.cargo /var/lib/apt/lists/*

WORKDIR /code

# Copy dependency files and install
COPY pyproject.toml uv.lock .
RUN uv pip install -r pyproject.toml --system

# Copy the rest of the project
COPY . .

# Copy entrypoint script
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Run migrations and start gunicorn
ENTRYPOINT ["/entrypoint.sh"]

