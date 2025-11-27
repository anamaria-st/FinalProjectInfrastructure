FROM python:3.12-slim

RUN apt-get update && apt-get install -y cron procps && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY cronjob /etc/cron.d/dailycron
RUN chmod 0644 /etc/cron.d/dailycron \
    && crontab /etc/cron.d/dailycron

RUN touch /var/log/cron.log

ENV FLASK_APP=app:create_app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

EXPOSE 5000

CMD ["sh", "-c", "cron -f & python -m flask run"]
