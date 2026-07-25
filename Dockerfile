FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
  && apt-get install -y --no-install-recommends ffmpeg \
  && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip \
  && python -m pip install -r /app/requirements.txt

COPY backend /app

CMD python manage.py migrate \
  && python manage.py collectstatic --noinput \
  && gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000}
