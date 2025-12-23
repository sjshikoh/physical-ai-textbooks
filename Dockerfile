# ---------------------------
# Base image
# ---------------------------
FROM python:3.10

# ---------------------------
# Environment settings
# ---------------------------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ---------------------------
# Working directory
# ---------------------------
WORKDIR /app

# ---------------------------
# System dependencies
# ---------------------------
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# ---------------------------
# Python dependencies
# ---------------------------
COPY requirements.txt .
RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# ---------------------------
# Copy application code
# ---------------------------
COPY ./backend/src ./src

# ---------------------------
# Expose HF Spaces port
# ---------------------------
EXPOSE 7860

# ---------------------------
# Run FastAPI app
# ---------------------------
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "7860"]

