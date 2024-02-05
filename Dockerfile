# Use an official Python runtime as a parent image
FROM python:3.11-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
  && apt-get install -y --no-install-recommends gcc \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip \
  && pip install -r requirements.txt

# Copy project
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Start Gunicorn
# Start Gunicorn, bind it to 0.0.0.0:80 (which listens on all interfaces, port 80)
CMD ["gunicorn", "--bind", "0.0.0.0:80", "curemeproject.wsgi:application"]