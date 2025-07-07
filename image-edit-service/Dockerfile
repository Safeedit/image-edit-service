# Use slim Python image
FROM python:3.11-slim

# Avoid prompts during build and set working directory
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# Install required OS libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose the correct port
EXPOSE 5000

# Start the Flask app
CMD ["python", "app.py"]
