# Use official Python image
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y build-essential libpq-dev libsqlite3-dev

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Run migrations
# RUN python manage.py migrate

# Create media and db directories
RUN mkdir -p /data/db
RUN mkdir -p /data/media

# Set environment variables
ENV DJANGO_SETTINGS_MODULE=chat_app.settings
ENV PYTHONPATH=/app

# Command to run Daphne for Channels
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "chat_app.asgi:application"]
