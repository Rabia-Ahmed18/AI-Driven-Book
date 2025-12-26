# Multi-stage Dockerfile for Backend Application with Railway Deployment Fix

# Build stage
FROM python:3.11-slim as builder

# Install system dependencies needed for building Python packages
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy the entire project first to ensure all files are available in the build context
COPY . .

# Now copy the requirements file from the project (should be available now)
COPY backend/requirements.txt requirements.txt

# Upgrade pip and install dependencies in a virtual environment
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt


# Runtime stage
FROM python:3.11-slim

# Install minimal system dependencies needed at runtime
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get autoremove -y \
    && apt-get clean

# Create a non-root user
RUN useradd --create-home --shell /bin/bash --uid 1000 appuser

# Copy the virtual environment from the builder stage
COPY --from=builder --chown=appuser:appuser /opt/venv /opt/venv

# Set working directory
WORKDIR /app

# Copy the application code
COPY --chown=appuser:appuser . .

# Make sure the non-root user owns the working directory
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Activate the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Set default environment variables
ENV PORT=8000
ENV PYTHONPATH=/app/backend/src

# Expose the port that the application will run on
EXPOSE 8000

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$PORT/health || exit 1

# Define the command to run the application
CMD ["sh", "-c", "python -m uvicorn app:app --host 0.0.0.0 --port $PORT"]