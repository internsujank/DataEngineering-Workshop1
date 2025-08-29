FROM python:3.10.2-alpine3.15

# Install system dependencies
RUN apk update && apk add --no-cache \
    postgresql-dev \
    gcc \
    python3-dev \
    musl-dev \
    libpq

# Copy requirements and install Python packages
COPY ./requirements.txt /tmp
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Create and switch to project directory
WORKDIR /root/workspace/src

# Copy project files
COPY . /root/workspace/src

# Expose port (optional, if you are running a web service)
EXPOSE 8000
