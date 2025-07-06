FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install OS dependencies for OpenCV and PIL
RUN apt-get update && \
    apt-get install -y libgl1 libglib2.0-0 && \
    pip install --no-cache-dir -r requirements.txt

# Expose the port Render will bind to (use 5000, not 5001)
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
