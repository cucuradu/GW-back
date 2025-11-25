FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for mysqlclient and psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY dcrm/dcrm/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY dcrm/dcrm /app

# Collect static files
RUN python manage.py collectstatic --no-input

# Expose port
EXPOSE 8000

# Run migrations and start server
CMD python manage.py migrate && gunicorn dcrm.wsgi:application --bind 0.0.0.0:8000
