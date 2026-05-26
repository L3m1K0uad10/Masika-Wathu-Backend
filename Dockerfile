FROM python:3.12-slim

# Preventing Python from creating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Displaying logs directly
ENV PYTHONUNBUFFERED=1

# Working directory
WORKDIR /app

# Installing PostgreSQL dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copying requirements first
COPY requirements.txt .

# Installing dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copying project files
COPY . .

# Expose Django port
EXPOSE 8000

# Run server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]