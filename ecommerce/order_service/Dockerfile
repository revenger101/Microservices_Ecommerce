FROM python:3.9

WORKDIR /app

# Install system dependencies including PostgreSQL client
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Add wait-for script
COPY wait-for.sh /wait-for.sh
RUN chmod +x /wait-for.sh

# Run migrations and start the service
CMD ["/bin/bash", "-c", "/wait-for.sh order_db:5432 -- python manage.py migrate && python orders/services.py"]