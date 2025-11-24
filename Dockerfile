FROM python:3.12-slim

# 1) Instalar cron y procps (para ps, top, etc.)
RUN apt-get update && apt-get install -y cron procps && rm -rf /var/lib/apt/lists/*

# 2) Directorio de trabajo
WORKDIR /app

# 3) Dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4) Copiar todo el proyecto
COPY . .

# 5) Copiar el cronjob y registrarlo
#    Asegúrate de que el archivo "cronjob" está en la raíz del proyecto
COPY cronjob /etc/cron.d/dailycron
RUN chmod 0644 /etc/cron.d/dailycron \
    && crontab /etc/cron.d/dailycron

# 6) Crear archivo de log para cron
RUN touch /var/log/cron.log

# 7) Variables de entorno para Flask
ENV FLASK_APP=app:create_app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

EXPOSE 5000

# 8) Arrancar cron en foreground y Flask en paralelo
CMD ["sh", "-c", "cron -f & python -m flask run"]

