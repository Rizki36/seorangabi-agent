FROM python:3.13-slim

WORKDIR /app

# Copy pyproject.toml first for better caching
COPY pyproject.toml ./

# Install the project in development mode
RUN pip install -e .
RUN pip install gunicorn

# Copy source code
COPY . .

# Expose the port the API runs on
EXPOSE 3021

# Start the API
CMD ["gunicorn", "--bind", "0.0.0.0:3021", "src.api:app"]