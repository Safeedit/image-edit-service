FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 5001

CMD ["python", "app.py"]
