# Bonzai Desktop - Production Dockerfile for Railway
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash bonzai
RUN chown -R bonzai:bonzai /app
USER bonzai

# Copy requirements first for better Docker caching
COPY --chown=bonzai:bonzai requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# Add user's local bin to PATH
ENV PATH="/home/bonzai/.local/bin:${PATH}"

# Copy application code
COPY --chown=bonzai:bonzai . .

# Create necessary directories
RUN mkdir -p /app/zai_memory /app/logs /tmp

# Set environment variables
ENV FLASK_APP=bonzai_app.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 5001

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5001/api/health || exit 1

# Start command with production settings
CMD ["python", "-m", "gunicorn", "--bind", "0.0.0.0:5001", "--workers", "2", "--worker-class", "eventlet", "--worker-connections", "1000", "--timeout", "120", "--keep-alive", "2", "--max-requests", "1000", "--max-requests-jitter", "50", "bonzai_app:app"]
