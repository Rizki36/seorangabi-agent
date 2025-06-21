FROM python:3.13-slim

WORKDIR /app

# Copy pyproject.toml first for better caching
COPY pyproject.toml ./

# Install the project in development mode
RUN pip install -e .

# Copy source code
COPY . .

# Expose the port the API runs on
EXPOSE 3021

# Start the API
CMD ["python", "-m", "src.api"]