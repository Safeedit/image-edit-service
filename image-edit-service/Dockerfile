# Base image with Python
FROM python:3.11-slim

# Avoid prompts during build and set working directory
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# Install required OS libraries for OpenCV and Pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies early to leverage Docker cache
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY . .

# Expose Flask port (Render uses 5000)
EXPOSE 5000

# Run your app
CMD ["python", "app.py"]
