# Use a modern Python image
FROM python:3.11-slim-bookworm

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies using uv
RUN uv sync --frozen --no-dev

# Expose API port
EXPOSE 8000

# Run the application
CMD ["uv", "run", "src/main.py"]
