FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast package management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy project files
COPY . .

# Install the project in editable mode for development, or just install it
RUN uv pip install --system .

# Set the environment variable for Gemini API Key (to be provided at runtime)
# ENV GEMINI_API_KEY=""

# Entrypoint is the ledge CLI
ENTRYPOINT ["ledge"]
CMD ["--help"]
