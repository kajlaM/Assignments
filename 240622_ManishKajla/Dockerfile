FROM python:3.10-slim

# Install system dependencies for FFmpeg and Manim (Pango/Cairo rendering backend)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    build-essential \
    python3-dev \
    libcairo2-dev \
    libpango1.0-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Add unprivileged user for security compliance (required by Hugging Face Spaces)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH
WORKDIR $HOME/app

# Pre-install dependencies for caching
COPY --chown=user requirements.txt $HOME/app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy application source files
COPY --chown=user . $HOME/app

# Command to boot the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
