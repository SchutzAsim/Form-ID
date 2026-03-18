FROM python:3.11-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy dependency files first for better caching
COPY pyproject.toml uv.lock* ./

# Install dependencies using uv
RUN uv sync --frozen --no-dev

# Copy the entire backend directory
COPY backend/ ./backend/

# Set Python path
ENV PYTHONPATH="/app:${PYTHONPATH}"

# Expose port
EXPOSE 8181

# Run the Python script directly (this will execute uvicorn.run())
CMD ["uv", "run", "python", "backend/main.py"]