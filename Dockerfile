FROM python:3.12-slim

# Instalar cron y procps (para ps)
RUN apt-get update && apt-get install -y cron procps

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Copiar cronjob
COPY cronjob /etc/cron.d/dailycron

# Permisos correctos
RUN chmod 0644 /etc/cron.d/dailycron
RUN crontab /etc/cron.d/dailycron

# Crear archivo de log
RUN touch /var/log/cron.log

ENV FLASK_APP=app:create_app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

EXPOSE 5000

# Iniciar cron en foreground y Flask en background
CMD cron -f & python -m flask run
