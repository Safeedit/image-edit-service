# Base image with Python
FROM python:3.11-slim

# Avoid prompts and set working dir
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# Optional: Use lightweight rembg model
ENV U2NET_MODEL_NAME=u2netp

# Install OS libraries needed for OpenCV/Pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose Flask port
EXPOSE 5000

# Optional healthcheck for observability
HEALTHCHECK CMD curl --fail http://localhost:5000 || exit 1

# Run the app
CMD ["python", "app.py"]
