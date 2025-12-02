FROM python:3.12-slim

# Cron para recordatorios
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1 \
    FLASK_APP=app:create_app \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_RUN_PORT=5000

EXPOSE 5000

# Por default, el web service usa este CMD
CMD ["python", "-m", "flask", "run"]
